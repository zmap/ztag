from ztag.annotation import Annotation, Type

from ztag import protocols


class IPPPrinter(Annotation):

    protocol = protocols.IPP
    subprotocol = protocols.IPP.BANNER
    port = None

    def process(self, obj, meta):
        meta.global_metadata.device_type = Type.PRINTER
        return meta
