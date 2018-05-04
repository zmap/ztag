from ztag.transform import ZGrabTransform, ZMapTransformOutput
from ztag import protocols, errors
from ztag.transform import Transformable
import https


class OracleTransform(ZGrabTransform):

    name = "oracle/generic"
    port = None
    protocol = protocols.ORACLE
    subprotocol = protocols.ORACLE.GENERIC

    def __init__(self, *args, **kwargs):
        super(OracleTransform, self).__init__(*args, **kwargs)

    def _transform_object(self, obj):
        zout = super(OracleTransform, self)._transform_object(obj)
        # No handshake -- just keep the TLS (if present).
        if "handshake" not in obj:
            return zout

        # Otherwise, just copy everything from handshake into the root.
        for k, v in obj["handshake"].items():
            zout.transformed[k] = v

        return zout
