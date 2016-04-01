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
        out["support"] = True

        t = data['data']['telnet']
        banner = t['banner'].resolve()
        if banner:
            out['banner'] = self.clean_banner(banner)
        will = t['will'].resolve()
        if will:
            out['will'] = will
        wont = t['wont'].resolve()
        if wont:
            out['wont'] = wont
        do = t['do'].resolve()
        if do:
            out['do'] = do
        dont = t['dont'].resolve()
        if dont:
            out['dont'] = dont

        if not out:
            raise errors.IgnoreObject("Empty output dict")

        out['ip_address'] = obj['ip']
        out['timestamp'] = obj['timestamp']
        zout = ZMapTransformOutput()
        zout.transformed = out
        return zout
