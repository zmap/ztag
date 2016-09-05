from ztag.transform import ZGrabTransform, ZMapTransformOutput
from ztag.transform import Transformable
from ztag import protocols, errors


class IMAPStartTLSTransform(ZGrabTransform):

    name = "imap/generic"
    port = None
    protocol = protocols.IMAP
    subprotocol = protocols.IMAP.STARTTLS

    def __init__(self, *args, **kwargs):
        super(IMAPStartTLSTransform, self).__init__(*args, **kwargs)

    def _transform_object(self, obj):

        zout = ZMapTransformOutput()
        wrapped = Transformable(obj)
        error_component = wrapped['error_component'].resolve()
        if error_component is not None and error_component == 'connect':
            raise errors.IgnoreObject("Error connecting") 

        banner = wrapped['data']['banner'].resolve()
        starttls = wrapped['data']['starttls'].resolve()

        try:
            tls_handshake = obj['data']['tls']
            out, certificates = tlsutil.make_tls_obj(tls_handshake)
            zout.transformed['tls'] = out
            zout.certificates = certificates

        except (TypeError, KeyError, IndexError):
            pass
        
        if banner is not None:
            zout.transformed['banner'] = self.clean_banner(banner)
        if starttls is not None:
            zout.transformed['starttls'] = self.clean_banner(starttls)

        if len(zout.transformed) == 0:
            raise errors.IgnoreObject("Empty Output dict")

        return zout


class IMAPSTransform(ZGrabTransform):

    name = "imaps/generic"
    port = 993
    protocol = protocols.IMAPS
    subprotocol = protocols.IMAPS.TLS

    def __init__(self, *args, **kwargs):
        super(IMAPSTransform, self).__init__(*args, **kwargs)

    def _transform_object(self, obj):
        zout = ZMapTransformOutput()
        wrapped = Transformable(obj)

        error_component = wrapped['error_component'].resolve()
        if error_component is not None and error_component == 'connect':
            raise errors.IgnoreObject("Error connecting") 

        banner = wrapped['data']['banner'].resolve()

        try:
            tls_handshake = obj['data']['tls']
            out, certificates = tlsutil.make_tls_obj(tls_handshake)
            zout.transformed['tls'] = out
            zout.certificates = certificates
        except (TypeError, KeyError, IndexError):
            pass
        
        if banner is not None:
            zout.transformed['banner'] = self.clean_banner(banner)

        if len(zout.transformed) == 0:
            raise errors.IgnoreObject("Empty Dict output")

        return zout
