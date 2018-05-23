from ztag.errors import IgnoreObject
from ztag.transform import ZGrab2Transform
from ztag import protocols


class OracleTransform(ZGrab2Transform):

    name = "oracle/banner"
    port = None
    protocol = protocols.ORACLE
    subprotocol = protocols.ORACLE.BANNER

    def __init__(self, *args, **kwargs):
        super(OracleTransform, self).__init__(*args, **kwargs)

    def clean_descriptor(self, desc):
        return [{
            "key": entry["key"],
            "value": self.clean_banner(entry["value"])
        } for entry in desc]

    def _transform_object(self, obj):
        # There shouldn't be a TLS object in this scan.
        zout = super(OracleTransform, self)._transform_object(obj, tls=False)
        results = self.get_scan_results(obj)
        if not results or "handshake" not in results:
            raise IgnoreObject("no results or no handshake")

        # Otherwise, just copy everything from handshake into the root.
        for k, v in results["handshake"].items():
            if v is None: continue
            if k == "refuse_error_raw":
                v = self.clean_banner(v)
            elif k == "refuse_error":
                v = self.clean_descriptor(v)
            zout.transformed[k] = v

        return zout
