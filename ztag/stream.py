import csv
import os
import sys
import time

from ztag.errors import IgnoreObject


class Stream(object):

    def __init__(self, incoming, outgoing, transforms=None, logger=None):
        super(Stream, self).__init__()
        self.incoming = incoming
        self.outgoing = outgoing
        self.transforms = transforms or list()
        self.logger = logger

    def run(self):
        skipped = 0
        handled = 0
        for obj in self.incoming:
            try:
                out = obj
                for transformer in self.transforms:
                    out = transformer.transform(out)
                    if out is None:
                        raise IgnoreObject()
                self.outgoing.take(out)
                handled += 1
            except IgnoreObject as e:
                if self.logger:
                    self.logger.debug(e.original_exception)
                    self.logger.trace(obj)
                skipped += 1
                continue
        self.outgoing.cleanup()
        return (handled, skipped)


class Incoming(object):
    pass


class InputFile(Incoming):

    def __init__(self, input_file=sys.stdin):
        self.input_file = input_file

    def __iter__(self):
        for line in self.input_file:
            yield line


class InputCSV(Incoming):

    def __init__(self, input_file=sys.stdin):
        self.input_file = input_file
        self.csvdict = csv.DictReader(self.input_file)

    def __iter__(self):
        for record in self.csvdict:
            yield record


class Outgoing(object):

    def __init__(self, *args, **kwargs):
        pass

    def take(self, obj):
        raise NotImplementedError

    def cleanup(self):
        pass


class PythonPrint(Outgoing):

    def __init__(self, *args, **kwargs):
        super(PythonPrint, self).__init__()

    def take(self, obj):
        print obj


class OutputFile(Outgoing):

    def __init__(self, output_file=sys.stdout, *args, **kwargs):
        super(OutputFile, self).__init__()
        self.output_file = output_file

    def take(self, obj):
        self.output_file.write(obj)
        self.output_file.write("\n")


class RedisQueue(Outgoing):

    CERTIFICATES_QUEUE = "certificate"
    PUBKEY_QUEUE = "pubkey"
    # we might as well try to do a whole bunch. The _worst_ case scenario
    # by setting a limit too high is that the server runs out of memory
    # and kills python and the task fails. Which would have happened
    # anyway, because we couldn't connect to redis.
    MAX_RETRIES = 60
    BATCH_SIZE = 250

    def __init__(self, logger=None, destination=None, *args, **kwargs):
        import redis
        super(RedisQueue, self).__init__(*args, **kwargs)
        host = os.environ.get('ZTAG_REDIS_HOST', 'localhost')
        port = int(os.environ.get('ZTAG_REDIS_PORT', 6379))
        if destination == "full_ipv4":
            queue = "ipv4"
        elif destination == "alexa_top1mil":
            queue = "domain"
        else:
            raise Exception("invalid destination: %s" % destination)
        self.logger = logger
        self.queue = queue
        try:
            self.redis = redis.Redis(host=host, port=port, db=0,
                                     socket_connect_timeout=10)
        except redis.ConnectionError as e:
            msg = "could not connect to redis: %s" % str(e)
            self.logger.fatal(msg)
        # batching
        self.queued = 0
        self.retries = 0
        self.records = []
        self.certificates = []

    def push(self, noretry=False):
        import redis
        if self.queued == 0:
            return
        try:
            p = self.redis.pipeline()
            for r in self.records:
                p.rpush(self.queue, r)
            for r in self.certificates:
                p.rpush(self.CERTIFICATES_QUEUE, r)
            p.execute()
            self.queued = 0
            self.records = []
            self.certificates = []
            self.retries = 0
        except redis.ConnectionError as e:
            time.sleep(1.0)
            self.retries += 1
            if self.retries > self.MAX_RETRIES or noretry:
                msg = "redis connection error: %s" % str(e)
                self.logger.fatal(msg)
                self.redis = None

    def take(self, pbout):
        self.records.append(pbout.transformed)
        self.certificates.extend(pbout.certificates)
        self.queued += (len(pbout.certificates) + 1)
        if self.queued > self.BATCH_SIZE:
            self.push()

    def cleanup(self):
        return self.push(noretry=True)


class Kafka(Outgoing):

    def __init__(self, logger=None, destination=None, *args, **kwargs):
        from kafka import KafkaProducer
        if destination == "full_ipv4":
            self.topic = "ipv4"
        elif destination == "alexa_top1mil":
            self.topic = "domain"
        else:
            raise Exception("invalid destination: %s" % destination)
        host = os.environ.get('KAFKA_BOOTSTRAP_HOST', 'localhost:9092')
        self.main_producer = KafkaProducer(bootstrap_servers=host)
        self.cert_producer = KafkaProducer(bootstrap_servers=host)

    def take(self, pbout):
        for certificate in pbout.certificates:
            self.cert_producer.send("certificate", certificate)
        self.main_producer.send(self.topic, pbout.transformed)

    def cleanup(self):
        if self.main_producer:
            self.main_producer.flush()
        if self.cert_producer:
            self.cert_producer.flush()


class Pubsub(Outgoing):

    def __init__(self, logger=None, destination=None, *args, **kwargs):
        import google
        from google.cloud import pubsub
        self.topic_url = os.environ.get('PUBSUB_DATA_TOPIC_URL')
        self.cert_topic_url = os.environ.get('PUBSUB_CERT_TOPIC_URL')
        if not self.topic_url:
            raise Exception('missing $PUBSUB_DATA_TOPIC_URL')
        if not self.cert_topic_url:
            raise Exception('missing $PUBSUB_CERT_TOPIC_URL')
        self.publisher = pubsub.PublisherClient()
        try:
            self.publisher.get_topic(self.topic_url)
            self.publisher.get_topic(self.cert_topic_url)
        except google.api_core.exceptions.GoogleAPICallError as e:
            logger.error(e.message)
            raise

    def take(self, pbout):
        for certificate in pbout.certificates:
            self.publisher.publish(self.cert_topic_url, certificate)
        self.publisher.publish(self.topic_url, pbout.transformed)

    def cleanup(self):
        # Not needed
        pass
