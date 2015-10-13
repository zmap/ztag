from ztag.annotation import *

class HeartbleedTag(Annotation):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.HEARTBLEED
    port = None

    def process(self, obj, meta):
        if obj["heartbleed_vulnerable"] is True:
            meta.tags.add("heartbleed")
            return meta
        return None
