import copy
from ztag.transform import Transform
from ztag.annotation import Annotation, Metadata
from ztag.device import Device

# Import the actual tags
# pylint: disable=W0401,W0614

class Annotator(Transform):

    def __init__(self, port, protocol, subprotocol, debug=False, logger=None):
        super(Annotator, self).__init__()
        self.eligible_tags = list()
        self.debug = debug
        self.logger = logger
        for tag_ in Annotation.iter():
            tag = tag_()
            if tag.check_port(port) and tag.check_protocol(protocol) \
                    and tag.check_subprotocol(subprotocol):
                self.eligible_tags.append(tag)

    def _transform_object(self, zobj):
        tags = set()
        metadata = dict()

        zobj.metadata = Metadata()
        d = zobj.transformed

        for tag in self.eligible_tags:
            try:
                meta = Metadata()
                meta = tag.process(d, meta)
                if meta is not None:
                    zobj.metadata.merge(meta)
            except Exception as e:
                if self.logger is not None:
                    self.logger.error(str(e))
                if self.debug:
                    raise e
        return zobj


class AnnotationTesting(object):

    def run(self, crash_on_failure):
        total = 0
        failures = 0
        have_tests = 0
        print "\n" + "="*25 + " ZTag Tests " + "="*25
        for A in sorted(Annotation.iter(), key=lambda x: x.__name__):
            total += 1
            annotation = A()
            tags_match = True
            local_metadata_match = True
            global_metadata_match = True
            errors = []
            if annotation.tests:
                have_tests += 1
                for k, v in annotation.tests.iteritems():
                    try:
                        d = Device.from_name(k).get(annotation.port, annotation.protocol, annotation.subprotocol)
                    except:
                        errors.append("  - %s uses a non-existent device" % k)
                        tags_match = local_metadata_match = global_metadata_match = False
                        if crash_on_failure:
                            raise
                        continue
                    if not d:
                        errors.append("  - %s does not have any data defined for the protocol targeted by this annotation" % k)
                        continue
                    input = copy.deepcopy(d)
                    if "metadata" in input:
                        del input["metadata"]
                    metadata = Metadata()
                    try:
                        output = annotation.process(input, metadata) or Metadata()
                    except:
                        errors.append("  - %s crashed during execution" % k)
                        tags_match = local_metadata_match = global_metadata_match = False
                        if crash_on_failure:
                            raise
                        continue
                    expected_tags = set(v.get("tags", []))
                    expected_global_metadata = v.get("global_metadata", {})
                    expected_local_metadata = v.get("local_metadata", {})
                    if set(output.tags) != set(expected_tags):
                        errors.append("  - %s (%s): %s != %s (expected)" % (k, "tags", str(output.tags), str(expected_tags)))
                        tags_match = False
                    if output.local_metadata.to_dict(with_description=False) != expected_local_metadata:
                        errors.append("  - %s (%s): %s != %s (expected)" % (k, "local metadata", str(output.local_metadata.to_dict()), str(expected_local_metadata)))
                        local_metadata_match = False
                    if output.global_metadata.to_dict(with_description=False) != expected_global_metadata:
                        errors.append("  - %s (%s): %s != %s (expected)" % (k, "global metadata", str(output.global_metadata.to_dict()), str(expected_global_metadata)))
                        global_metadata_match = False
                if errors:
                    print "{0}: \033[01;31mfail\033[00m".format(annotation.__class__.__name__)
                    for error in errors:
                        print error
                    failures += 1
                else:
                    print "{0}: \033[1;92m{1}\033[00m".format(annotation.__class__.__name__, "success")
            else:
                print "{0}: \033[1;94mno tests\033[00m".format(annotation.__class__.__name__)
        # print summary information
        print "\n" + "="*25 + " Summary " + "="*25 + "\n"
        print "annotation modules loaded: %i/%i" % (Annotation._annotation_annotations_total - Annotation._annotation_annotations_fail, Annotation._annotation_annotations_total)
        print "test coverage: %i/%i" % (have_tests, total)
        print "tests passing: %i/%i" % (have_tests - failures, have_tests)
        print "\n"
        return 1 if failures or Annotation._annotation_annotations_fail else 0

