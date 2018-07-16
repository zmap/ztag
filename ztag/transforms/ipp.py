from ztag.transform import ZGrab2Transform
from ztag import protocols


class IPPTransform(ZGrab2Transform):

    name = "ipp/banner"
    port = 631
    protocol = protocols.IPP
    subprotocol = protocols.IPP.BANNER

    def __init__(self, *args, **kwargs):
        super(IPPTransform, self).__init__(*args, **kwargs)

    def _transform_object(self, obj):
        zout = super(IPPTransform, self)._transform_object(obj)
        results = self.get_scan_results(obj)
        if not results:
            return zout

        to_copy = ["version_major", "version_minor", "version_string", "cups_version", "attributes", "attr_cups_version", "attr_ipp_versions", "attr_printer_uris"]

        for f in to_copy:
            if results.get(f) is not None:
                zout.transformed[f] = results[f]

        to_clean = []
        for f in to_clean:
            if f in zout.transformed:
                zout.transformed[f] = self.clean_banner(zout.transformed[f])

        return zout