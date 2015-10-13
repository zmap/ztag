from ztag.transform import ZGrabTransform, ZMapTransformOutput
import https
from ztag.transform import Transformable

from ztag import protocols, errors


class POP3StartTLSTransform(ZGrabTransform):

    name = "pop3/generic"
    port = None
    protocol = protocols.POP3
    subprotocol = protocols.POP3.STARTTLS

    def _transform_object(self, obj):

        wrapped = Transformable(obj)

        error_component = wrapped['error_component'].resolve()
        if error_component is not None and error_component == 'connect':
            raise errors.IgnoreObject("Error connecting")

        banner = wrapped['data']['banner'].resolve()
        starttls = wrapped['data']['starttls'].resolve()
        
        zout = ZMapTransformOutput()
        try:
            tls_handshake = obj['data']['tls']
            out, certificates = https.HTTPSTransform.make_tls_obj(tls_handshake)
            zout.transformed['tls'] = out
            zout.certificates = certificates
        except (TypeError, KeyError, IndexError):
            pass

        if banner is not None:
            zout.transformed['banner'] = self.clean_banner(banner)
        if starttls is not None:
            zout.transformed['starttls'] = self.clean_banner(starttls)
        
        if len(zout.transformed) == 0:
            raise errors.IgnoreObject("Empty output dict")

        return zout


class POP3STransform(ZGrabTransform):

    name = "pop3s/generic"

    port = 995
    protocol = protocols.POP3S
    subprotocol = protocols.POP3S.TLS

    def __init__(self, *args, **kwargs):
        super(POP3STransform, self).__init__(*args, **kwargs)

    def _transform_object(self, obj):
        wrapped = Transformable(obj)

        error_component = wrapped['error_component'].resolve()
        if error_component is not None and error_component == 'connect':
            raise errors.IgnoreObject("Error connecting")

        banner = wrapped['data']['banner'].resolve()

        zout = ZMapTransformOutput()
        try:
            tls_handshake = obj['data']['tls']
            out, certificates = https.HTTPSTransform.make_tls_obj(tls_handshake)
            zout.transformed['tls'] = out
            zout.certificates = certificates
        except (TypeError, KeyError, IndexError):
            pass

        if banner is not None:
            zout.transformed['banner'] = self.clean_banner(banner)
        
        if len(zout.transformed) == 0:
            raise errors.IgnoreObject("Empty output dict")

        return zout
