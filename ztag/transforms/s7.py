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
        if not s['is_s7'].resolve() or not s.resolve():
            raise errors.IgnoreObject()
        out = s.resolve()
        out['support'] = True
        del out['is_s7']
        zout.transformed = out
        return zout
