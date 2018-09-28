import csv
import os
import sys
import time
import collections
import threading
import logging

from ztag.errors import IgnoreObject


class Updater(object):
    """
    Updater encapsulates the behavior for the updates.csv file; put_update() is called with each
    update, but output is only written every :frequency: seconds.
    """
    def __init__(self, output=None, frequency=1.0, logger=None):
        self.output = output
        self.frequency = frequency
        self.logger = logger
        self.prev = None
        self._wrote_labels = False

    def put_update(self, row):
        if not self.output:
            return

        if self.prev and (row.time - self.prev.time) < self.frequency:
            return

        self.prev = row

        if not self._wrote_labels:
            self.output.write(row.get_csv_labels() + "\n")
            self._wrote_labels = True

        self.output.write(row.get_csv() + "\n")
        self.output.flush()

    def close(self):
        if self.output and self.output != sys.stderr:
            try:
                self.output.close()
            except BaseException as e:
                if self.logger:
                    self.logger.warn("Failed to close updates CSV stream: %s", str(e))


class UpdateRow(object):
    """
    UpdateRow encapsulates the information for a single update and the logic for outputting it as
    a CSV row.
    """
    ORDER = ("skipped", "handled", "delta_skipped", "delta_handled")

    def __init__(self, skipped, handled, updated_at=None, prev=None):
        """
        Construct a new row with the given number of skipped / handled entries, and calculate the
        deltas from prev (or set them to 0). Also sets time to now.
        :param skipped: current total number of skipped records
        :param handled: current total number of handled records
        :param prev: the previous UpdateRow
        """
        self.time = updated_at or time.time()
        self.skipped = skipped
        self.handled = handled
        if prev:
            self.delta_skipped = skipped - prev.skipped
            self.delta_handled = handled - prev.handled
        else:
            self.delta_skipped = 0
            self.delta_handled = 0

    @classmethod
    def get_csv_labels(cls):
        return ",".join(cls.ORDER)

    def get_csv(self):
        return ",".join(str(getattr(self, label)) for label in self.ORDER)


class Stream(object):

    def __init__(self, incoming, outgoing, transforms=None, logger=None, updates=None):
        super(Stream, self).__init__()
        self.incoming = incoming
        self.outgoing = outgoing
        self.transforms = transforms or list()
        self.logger = logger
        if updates:
            self.updater = Updater(output=updates, frequency=1.0, logger=logger)
        else:
            self.updater = None

    def put_update(self, skipped, handled):
        if not self.updater:
            return
        this_update = UpdateRow(skipped=skipped, handled=handled, prev=self.updater.prev)
        self.updater.put_update(this_update)

    def run(self):
        skipped = 0
        handled = 0
        for obj in self.incoming:
            self.put_update(handled=handled, skipped=skipped)
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
                    if e.trback:
                        self.logger.warn(e.trback)
                skipped += 1
                continue
        self.outgoing.cleanup()
        if self.updater:
            self.updater.close()
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

failed_msg_t = collections.namedtuple('failed_msg_t', 'topic msg attempt')

class PubsubState():
    '''
    Hold state with single course-grained lock. Restrict to safe operations
    on shared memory.
    '''

    def __init__(self):
        self._lock = threading.Lock()
        self._npending_msgs = 0
        self._failed_msgs = []

        # An individual thread raising an exception or calling
        # sys.exit() will only end that thread. Use this to
        # signal the rest of the threads to exit.
        self.exit_exception = None

    def inc_npending(self):
        self._lock.acquire()
        self._npending_msgs += 1
        self._lock.release()

    def dec_npending(self):
        self._lock.acquire()
        self._npending_msgs -= 1
        self._lock.release()

    def get_npending(self):
        '''
        No lock required to simply read int; no direct writes allowed.
        '''
        return self._npending_msgs

    def add_failed_msg(self, topic, msg, attempt):
        self._lock.acquire()
        self._failed_msgs.append(failed_msg_t(topic, msg, attempt))
        self._lock.release()

    def retrieve_failed_msgs(self):
        '''
        Retrieve list of failed messages and reset running list. Returned
        value is no longer shared data.
        '''
        self._lock.acquire()
        retval = self._failed_msgs
        self._failed_msgs = []
        self._lock.release()
        return retval

class Pubsub(Outgoing):

    MAX_ATTEMPTS = 5

    def __init__(self, logger=None, destination=None, *args, **kwargs):
        import google
        from google.cloud import pubsub, pubsub_v1
        self.logger = logger
        if logger is None:
            self.logger = logging.getLogger('null-logger')
            self.logger.setLevel(9999)
        if destination == "full_ipv4":
            self.topic_url = os.environ.get('PUBSUB_IPV4_TOPIC_URL')
        elif destination == "alexa_top1mil":
            self.topic_url = os.environ.get('PUBSUB_ALEXA_TOPIC_URL')
        self.cert_topic_url = os.environ.get('PUBSUB_CERT_TOPIC_URL')
        if not self.topic_url:
            raise Exception('missing $PUBSUB_[IPV4|ALEXA]_TOPIC_URL')
        if not self.cert_topic_url:
            raise Exception('missing $PUBSUB_CERT_TOPIC_URL')
        batch_settings = pubsub_v1.types.BatchSettings(
            # "The entire request including one or more messages must
            #  be smaller than 10MB, after decoding."
            max_bytes=8192000,  # 8 MB
            max_latency=15,     # 15 seconds
        )
        self.publisher = pubsub.PublisherClient(batch_settings)
        self.publish_count = {}
        try:
            self.publisher.get_topic(self.topic_url)
            self.publisher.get_topic(self.cert_topic_url)
        except google.api_core.exceptions.GoogleAPICallError as e:
            logger.error(e.message)
            raise
        self._state = PubsubState()

    def _make_done_callback(self, topic, data, attempt):
        def done_callback(future):
            if self._state.exit_exception:
                sys.exit(1)
            exception = future.exception()
            if not exception:
                self.logger.debug("Publish attempt #{attempt}/{max} on topic '{topic}' "
                                  "succeeded.".format(attempt=attempt + 1,
                                                      max=self.MAX_ATTEMPTS,
                                                      topic=topic))
                self._state.dec_npending()
            else:
                self.logger.error("Publish attempt #{attempt}/{max} failed for data '{data}' on"
                                  "topic '{topic}' {error}"
                                  .format(attempt=attempt + 1,
                                          max=self.MAX_ATTEMPTS,
                                          data=data,
                                          topic=topic,
                                          error=str(exception)))
                if attempt >= self.MAX_ATTEMPTS:
                    self._state.exit_exception = exception
                    sys.exit(1)
                self._state.add_failed_msg(topic, data, attempt + 1)

        return done_callback

    def _publish_with_callback(self, topic, data, attempt):
        if attempt == 0:
            self._state.inc_npending()
        cb = self._make_done_callback(topic, data, attempt)
        publish_future = self.publisher.publish(topic, data)
        publish_future.add_done_callback(cb)

    def take(self, pbout):
        for certificate in pbout.certificates:
            self._publish_with_callback(self.cert_topic_url, certificate, 0)
        self._publish_with_callback(self.topic_url, pbout.transformed, 0)

    def cleanup(self):
        while self._state.get_npending() > 0:
            time.sleep(10)
            if self._state.exit_exception:
                self.logger.error("Max attempts exceeded; raising most recent exception.")
                raise self._state.exit_exception
            failed_msgs = self._state.retrieve_failed_msgs()
            self.logger.debug("Failed message queuelen: {}, "
                              "messages pending: {}"
                              .format(len(failed_msgs),
                                      self._state.get_npending()))
            for failed in failed_msgs:
                self._publish_with_callback(failed.topic, failed.msg,
                                            failed.attempt + 1)
        self.logger.debug("Pubsub cleanup: Finished.")
