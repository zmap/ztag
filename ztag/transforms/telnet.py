from ztag import protocols, errors
from ztag.transform import *

class TelnetTransform(ZGrabTransform):

    name = "telnet/banner"
    port = 23
    protocol = protocols.TELNET
    subprotocol = protocols.TELNET.BANNER

    def _transform_object(self, obj):
        if "error" in obj:
            raise errors.IgnoreObject("Error")

        data = Transformable(obj)
        out = dict()

        banner = out['data']['banner'].resolve()
        if banner:
            out['banner'] = self.clean_banner(banner)
        will = out['data']['will'].resolve()
        if will:
            out['will'] = will
        wont = out['data']['wont'].resolve()
        if wont:
            out['wont'] = wont
        do = out['data']['do'].resolve()
        if do:
            out['do'] = do
        dont = out['data']['dont'].resolve()
        if dont:
            out['dont'] = dont

        if not out:
            raise errors.IgnoreObject("Empty output dict")

        out['ip_address'] = obj['ip']
        out['timestamp'] = obj['timestamp']
        zout = ZMapTransformOutput()
        zout.transformed = out
        return zout
