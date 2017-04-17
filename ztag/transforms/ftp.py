from ztag.transform import ZGrabTransform, ZMapTransformOutput
from ztag import protocols, errors
from ztag.transform import Transformable

class FTPTransform(ZGrabTransform):

    name = "ftp/generic"
    port = 21
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER

    def __init__(self, *args, **kwargs):
        super(FTPTransform, self).__init__(*args, **kwargs)

    def _transform_object(self, obj):
        ftp_banner = obj
        ftp = Transformable(obj)
        zout = ZMapTransformOutput()
        error = ftp['error'].resolve()
        if error is not None:
            raise errors.IgnoreObject("Error")
        out = dict()
        banner = ftp['data']['banner'].resolve()

        if banner is not None:
            out['banner'] = self.clean_banner(banner)

        if len(out) == 0:
            raise errors.IgnoreObject("Empty output dict")
        out['ip_address'] = obj['ip']
        out['timestamp'] = obj['timestamp']
        zout.transformed = out
        return zout

class FTPSTransform(ZGrabTransform):
    name = "ftp/ftps"
    port = 21
    protocol = protocols.FTP
    subprotocol = protocols.TLS

    def __init__(self, *args, **kwargs):
        super(FTPTransform, self).__init__(*args, **kwargs)

    def _transform_object(self, obj):
        ftp_banner = obj
        ftp = Transformable(obj)
        zout = ZMapTransformOutput()
        error = ftp['error'].resolve()
        if error is not None:
            raise errors.IgnoreObject("Error")

        out = dict()
        banner = ftp['data']['ftp']['banner'].resolve()

        if banner is not None:
            out['banner'] = self.clean_banner(banner)

        if len(out) == 0:
            raise errors.IgnoreObject("Empty output dict")

        out['ip_address'] = obj['ip']
        out['timestamp'] = obj['timestamp']
        zout.transformed = out
        return zout
