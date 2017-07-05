from ztag.transform import *
from ztag import protocols, errors

class SMBTransform(ZGrabTransform):

    name="smb/status"
    port = 445
    protocol = protocols.SMB
    subprotocol = protocols.SMB.BANNER

    def _transform_object(self, obj):
        zout = ZMapTransformOutput()
        wrapped = Transformable(obj)
        smb = wrapped['data']['smb']
        if not smb['smbv1_support'].resolve():
            raise errors.IgnoreObject()
        out = {
            "smbv1_support": smb['smbv1_support'].resolve()
        }
        zout.transformed = out
        return zout
