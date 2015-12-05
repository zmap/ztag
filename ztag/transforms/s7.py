from ztag.transform import *
from ztag import protocols, errors


class S7Transform(ZGrabTransform):

    name = "s7/status"
    port = 102
    protocol = protocols.S7
    subprotocol = protocols.S7.SZL


    def _transform_object(self, obj):
        zout = ZMapTransformOutput()
        wrapped = Transformable(obj)
        s = wrapped['data']['s7']
        if not s['is_dnp3'].resolve() or not s.resolve():
            raise errors.IgnoreObject()
        s = s.resolve()
        out = {
            "support": True,
        }
        for key, value in s.iteritems():
            if key == "is_dnp3":
                continue
            out[key] = value
        zout.transformed = out
        return zout
