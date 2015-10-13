from ztag.transform import ZGrabTransform, ZMapTransformOutput
from ztag import protocols, errors
from ztag.transform import Transformable
import https


class SMTPStartTLSTransform(ZGrabTransform):

    name = "smtp/generic"
    port = None
    protocol = protocols.SMTP
    subprotocol = protocols.SMTP.STARTTLS

    def __init__(self, *args, **kwargs):
        super(SMTPStartTLSTransform, self).__init__(*args, **kwargs)

    def _transform_object(self, obj):

        wrapped = Transformable(obj)
        error_component = wrapped['error_component'].resolve()
        if error_component is not None and error_component == 'connect':
            raise errors.IgnoreObject("Error connecting")

        banner = wrapped['data']['banner'].resolve()
        ehlo = wrapped['data']['ehlo'].resolve()
        starttls = wrapped['data']['starttls'].resolve()

        zout = ZMapTransformOutput()
        try:
            tls_handshake = obj['data']['tls']
            out, certificates  = https.HTTPSTransform.make_tls_obj(tls_handshake)
            zout.transformed['tls'] = out
            zout.certificates = certificates
        except (KeyError, TypeError, IndexError):
            pass

        if banner is not None:
            zout.transformed['banner'] = self.clean_banner(banner)
        if ehlo is not None:
            zout.transformed['ehlo'] = self.clean_banner(ehlo)
        if starttls is not None:
            zout.transformed['starttls'] = self.clean_banner(starttls)
        
        if len(zout.transformed) == 0:
            raise errors.IgnoreObject("Empty output dict")

        return zout


class SMTPSTransform(ZGrabTransform):

    name = "smtps/generic"
    port = None
    protocol = protocols.SMTPS
    subprotocol = protocols.SMTPS.TLS

    def __init__(self, *args, **kwargs):
        super(SMTPSTransform, self).__init__(*args, **kwargs)

    def _transform_object(self, obj):
        tls_handshake = obj['log'][1]['data']
        banner = obj['log'][2]['banner']
        ehlo = obj['log'][3]['response']
        out = https.HTTPSTransform.make_tls_obj(tls_handshake)
        out['banner'] = self.clean_banner(banner)
        out['ehlo'] = self.clean_banner(ehlo)
        out['ip_address'] = obj['host']
        out['timestamp'] = obj['time']
        return out
