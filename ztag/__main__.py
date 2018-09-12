import argparse
import sys
import json

from zsearch_definitions import protocols

from ztag.stream import Stream, Incoming, Outgoing, InputFile, OutputFile
from ztag.transform import Transform, Decoder, Encoder
from ztag.decoders import JSONDecoder
from ztag.encoders import JSONEncoder
from ztag.annotation import Annotation
from ztag.annotator import Annotator, AnnotationTesting
from ztag.transformer import ZMapTransformer
from ztag.log import Logger
from ztag.classargs import subclass_of

from datetime import datetime


def non_negative(s):
    x = int(s)
    if x < 0:
        raise argparse.ArgumentTypeError
    return x


def uint16(s):
    x = int(s)
    if x < 0 or x > 65535:
        raise argparse.ArgumentTypeError
    return x


def zsearch_protocol(s):
    try:
        return protocols.Protocol.from_pretty_name(s)
    except KeyError as e:
        raise argparse.ArgumentTypeError(e)


def zsearch_subprotocol(s):
    try:
        return protocols.Subprotocol.from_pretty_name(s)
    except KeyError as e:
        raise argparse.ArgumentTypeError(e)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=uint16,
                        help="Target port")
    parser.add_argument('-P', '--protocol',
                        type=zsearch_protocol)
    parser.add_argument('-S', '--subprotocol',
                        type=zsearch_subprotocol)
    parser.add_argument('-T', '--destination', default="full_ipv4",
                        type=str, choices=["full_ipv4", "alexa_top1mil"])
    parser.add_argument('-s', '--scan-id', required=False, type=non_negative)
#   parser.add_argument('-t', '--tags', type=tag_class)
    parser.add_argument('-I', '--incoming', type=subclass_of(Incoming),
                        default=None)
    parser.add_argument('-D', '--decoder', type=subclass_of(Decoder),
                        default=JSONDecoder)
    parser.add_argument('-X', '--transform', type=subclass_of(Transform),
                        default=None)
    parser.add_argument('-E', '--encoder', type=subclass_of(Encoder),
                        default=JSONEncoder)
    parser.add_argument('-O', '--outgoing', type=subclass_of(Outgoing),
                        default=OutputFile)
    parser.add_argument('-i', '--input-file', default=sys.stdin,
                        type=argparse.FileType('r'))
    parser.add_argument('-l', '--log-file', type=argparse.FileType('w'),
                        default=sys.stderr)
    parser.add_argument('--updates-file', default=sys.stderr,
                        type=argparse.FileType('w'))
    parser.add_argument('-v', '--log-level', type=int, default=Logger.INFO,
                        choices=range(0, Logger.TRACE + 1))
    parser.add_argument('-m', '--metadata-file', type=argparse.FileType('w'),
                        default=sys.stderr)
    parser.add_argument('--strip-domain-prefix', type=str, default=None)
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-t', '--tests', action='store_true')
    parser.add_argument('--safe-import', action='store_true')
    parser.add_argument('--no-safe-tests', action='store_true')
    args = parser.parse_args()

    Annotation.load_annotations(args.safe_import)

    if args.tests:
        sys.exit(AnnotationTesting().run(args.no_safe_tests))

    if not args.port:
        sys.stderr.write("ERROR: port (-p/--port) required\n")
        sys.exit(1)
    if not args.protocol:
        proto_string = ", ".join(protocols.Protocol._by_pretty_name.keys())
        sys.stderr.write("ERROR: protocol (-P/--protocol) required\n")
        sys.stderr.write("Registered Protocols: %s\n" % proto_string)
        sys.exit(1)
    if not args.subprotocol:
        subproto_string = ", ".join(
            protocols.Subprotocol._by_pretty_name.keys())
        sys.stderr.write("ERROR: subprotocol (-S/--subprotocol) required\n")
        sys.stderr.write("Registered SubProtocols: %s\n" % subproto_string)
        sys.exit(1)

    metadata = dict()

    port = args.port
    protocol = args.protocol
    subprotocol = args.subprotocol
    scan_id = args.scan_id or 0
    transform_kwargs = dict()
    transform_args = list()

    logger = Logger(args.log_file, log_level=args.log_level)

    if args.strip_domain_prefix:
        if not args.strip_domain_prefix.endswith("."):
            args.strip_domain_prefix += "."
        logger.info("stripping prefix %s" % args.strip_domain_prefix)
        transform_kwargs['strip_domain_prefix'] = args.strip_domain_prefix

    if args.transform is not None:
        transform = args.transform(port, protocol, subprotocol, scan_id,
                                   *transform_args, **transform_kwargs)
    else:
        transform = ZMapTransformer.find_transform(port, protocol, subprotocol,
                                                   scan_id, *transform_args, **transform_kwargs)
    if args.incoming is not None:
        incoming = args.incoming(input_file=args.input_file)
    elif transform.incoming is not None:
        incoming = transform.incoming(input_file=args.input_file)
    else:
        incoming = InputFile(input_file=args.input_file)

    if args.decoder is not None:
        decoder = args.decoder(logger=logger)
    elif transform.decoder is not None:
        decoder = transform.decoder(logger=logger)
    else:
        decoder = JSONDecoder(logger=logger)

    encoder = args.encoder(port, protocol, subprotocol, scan_id)
    outgoing = args.outgoing(output_file=sys.stdout, logger=logger,
                             destination=args.destination)

    tagger = Annotator(port, protocol, subprotocol,
                       debug=args.debug, logger=logger)
    num_tags = len(tagger.eligible_tags)
    logger.info("found %d tags" % num_tags)
    metadata['eligible_tags'] = num_tags

    transforms = [
        decoder,
        transform,
        tagger,
        encoder,
    ]
    s = Stream(incoming, outgoing, transforms=transforms, logger=logger, updates=args.updates_file)
    start_time = datetime.utcnow()

    handled, skipped = s.run()

    end_time = datetime.utcnow()
    duration = end_time - start_time

    logger.info("handled %d records" % handled)
    logger.info("skipped %d records" % skipped)

    metadata['records_handled'] = handled
    metadata['records_skipped'] = skipped
    metadata['start_time'] = Logger.rfc_time_from_utc(start_time)
    metadata['end_time'] = Logger.rfc_time_from_utc(end_time)
    metadata['duration'] = int(duration.total_seconds())

    args.metadata_file.write(json.dumps(metadata))
    args.metadata_file.write("\n")
    args.metadata_file.flush()


if __name__ == "__main__":
    main()
