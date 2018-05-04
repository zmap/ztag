from ztag.transform import ZGrab2Transform
from ztag import protocols


class OracleTransform(ZGrab2Transform):

    name = "oracle/generic"
    port = None
    protocol = protocols.ORACLE
    subprotocol = protocols.ORACLE.GENERIC

    def __init__(self, *args, **kwargs):
        super(OracleTransform, self).__init__(*args, **kwargs)

    def _transform_object(self, obj):
        zout = super(OracleTransform, self)._transform_object(obj)
        results = self.get_scan_results(obj)
        # No handshake -- just keep the TLS (if present).
        if not results or "handshake" not in results:
            return zout

        # Otherwise, just copy everything from handshake into the root.
        for k, v in results["handshake"].items():
            zout.transformed[k] = v

        return zout
