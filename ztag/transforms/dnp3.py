from ztag.transform import *
from ztag import protocols, errors

class DNP3Transform(ZGrabTransform):

    name = "dnp3/status"
    port = 20000
    protocol = protocols.DNP3
    subprotocol = protocols.DNP3.STATUS

    def _transform_object(self, obj):
        zout = ZMapTransformOutput()
        wrapped = Transformable(obj)
        dnp3 = wrapped['data']['dnp3']
        if not dnp3['is_dnp3'].resolve():
            raise errors.IgnoreObject()
        out = {
            "support": True,
            "raw_response": dnp3["raw_response"].resolve(),
        }
        zout.transformed = out
        return zout
