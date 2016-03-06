from ztag.transform import ZGrabTransform, ZMapTransformOutput
from ztag import protocols, errors
from ztag.transform import Transformable
from ztag.errors import IgnoreObject


class SSLv2Transform(ZGrabTransform):

    name = "*/sslv2"
    port = None
    protocol = {
        protocols.HTTPS,
        protocols.SMTP,
        protocols.SMTPS,
        protocols.IMAP,
        protocols.IMAPS,
        protocols.POP3,
        protocols.POP3S,
    }
    subprotocol = protocols.HTTPS.SSL_2


    def __init__(self, *args, **kwargs):
        super(SSLv2Transform, self).__init__(*args, **kwargs)

    def _transform_object(self, obj):
        wrapped = Transformable(obj['data'])
        ciphers = wrapped['sslv2']['server_hello']['ciphers'].resolve()
        certificate = wrapped['sslv2']['server_hello']['certificate'].resolve()
        sslv2_support = bool(wrapped['sslv2']['server_verify'].resolve())
        sslv2_export = bool(wrapped['sslv2_export']['server_verify'].resolve())
        sslv2_extra_clear = bool(wrapped['sslv2_extra_clear']['server_verify']
                ['extra_clear'].resolve())
        out = {
            'support': sslv2_support,
            'export': sslv2_export,
            'extra_clear': sslv2_extra_clear,
        }
        if ciphers is not None:
            out['ciphers'] = ciphers
        if certificate is not None:
            out['certificate'] = {
                'parsed': certificate['parsed']
            }
            certificates = [certificate]
        else:
            certificates = list()

        zout = ZMapTransformOutput()
        zout.transformed = out
        zout.certificates = certificates
        return zout
