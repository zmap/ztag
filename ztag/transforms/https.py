from ztag.transform import ZGrabTransform, ZMapTransformOutput
from ztag import protocols, errors
from ztag.transform import Transformable
from ztag.errors import IgnoreObject
import tlsutil


class HTTPSTransform(ZGrabTransform):

    name = "https/generic"
    port = None
    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS

    def __init__(self, *args, **kwargs):
        super(HTTPSTransform, self).__init__(*args, **kwargs)

    def _transform_object(self, obj):
        tls = obj['data']['tls']
        out, certificates = tlsutil.make_tls_obj(tls)
        zout = ZMapTransformOutput()
        zout.transformed = out
        zout.certificates = certificates
        return zout

class HeartbleedTransform(ZGrabTransform):

    name = "https/heartbleed"
    port = None
    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.HEARTBLEED

    def __init__(self, *args, **kwargs):
        super(HeartbleedTransform, self).__init__(*args, **kwargs)

    def _transform_object(self, obj):
        zout = ZMapTransformOutput()
        out = dict()

        wrapped = Transformable(obj)

        error_component = wrapped['error_component'].resolve()
        if error_component is not None and error_component == 'connect':
            raise errors.IgnoreObject("Error connecting")

        heartbleed = wrapped['data']['heartbleed']
        heartbleed = wrapped['data']['heartbleed']

        heartbleed_enabled = heartbleed['heartbeat_enabled'].resolve()
        heartbleed_vulnerable = heartbleed['heartbleed_vulnerable'].resolve()
        if heartbleed_enabled is not None:
            out['heartbeat_enabled'] = heartbleed_enabled
        if heartbleed_vulnerable is not None:
            out['heartbleed_vulnerable'] = heartbleed_vulnerable

        if len(out) == 0:
            raise errors.IgnoreObject("Empty Output dict")

        zout.transformed = out
        return zout


class SSLv3Transform(ZGrabTransform):

    name = "https/sslv3"
    port = None
    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.SSL_3

    def __init__(self, *args, **kwargs):
        super(SSLv3Transform, self).__init__(*args, **kwargs)

    def _transform_object(self, obj):
        zout = ZMapTransformOutput()
        tempout = dict()
        wrapped = Transformable(obj)
        error_component = wrapped['error_component'].resolve()
        if error_component is not None and error_component == 'connect':
            raise errors.IgnoreObject("Error connecting")

        tls_handshake = wrapped['data']['tls']
        value = tls_handshake['server_hello']['version']['value'].resolve()
        out = dict()
        if value is not None:
            version = int(value)
            out['support'] = True if version == 768 else False
        else:
            raise errors.IgnoreObject("Empty Output dict")

        zout.transformed = out
        return zout


class TLSv10Transform(ZGrabTransform):
    name = "https/tls10"
    port = None
    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS_1_0

    def __init__(self, *args, **kwargs):
        super(TLSv10Transform, self).__init__(*args, **kwargs)

    def _transform_object(self, obj):
        zout = ZMapTransformOutput()
        tempout = dict()
        wrapped = Transformable(obj)

        error_component = wrapped['error_component'].resolve()
        if error_component is not None and error_component == 'connect':
            raise errors.IgnoreObject("Error connecting")

        tls_handshake = wrapped['data']['tls']
        value = tls_handshake['server_hello']['version']['value'].resolve()
        out = dict()
        if value is not None:
            version = int(value)
            out['support'] = True if version == 769 else False
        else:
            raise errors.IgnoreObject("Empty output dict")

        zout.transformed = out
        return zout


class TLSv11Transform(ZGrabTransform):
    name = "https/tls11"
    port = None
    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS_1_1

    def __init__(self, *args, **kwargs):
        super(TLSv11Transform, self).__init__(*args, **kwargs)

    def _transform_object(self, obj):
        zout = ZMapTransformOutput()
        tempout = dict()
        wrapped = Transformable(obj)
        error_component = wrapped['error_component'].resolve()
        if error_component is not None and error_component == 'connect':
            raise errors.IgnoreObject("Error connecting")
        tls_handshake = wrapped['data']['tls']
        value = tls_handshake['server_hello']['version']['value'].resolve()
        out = dict()
        if value is not None:
            version = int(value)
            out['support'] = True if version == 770 else False
        else:
            raise errors.IgnoreObject("Empty Output dict")

        zout.transformed = out
        return zout


class TLSv12Transform(ZGrabTransform):
    name = "https/tls12"
    port = None
    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS_1_2

    def __init__(self, *args, **kwargs):
        super(TLSv12Transform, self).__init__(*args, **kwargs)

    def _transform_object(self, obj):
        zout = ZMapTransformOutput()
        tempout = dict()
        wrapped = Transformable(obj)
        error_component = wrapped['error_component'].resolve()
        if error_component is not None and error_component == 'connect':
            raise errors.IgnoreObject("Error connecting")
        tls_handshake = wrapped['data']['tls']
        value = tls_handshake['server_hello']['version']['value'].resolve()
        out = dict()
        if value is not None:
            version = int(value)
            out['support'] = True if version == 771 else False
        else:
            raise errors.IgnoreObject("Empty Output Dict")

        zout.transformed = out
        return zout


class TLSv13Transform(ZGrabTransform):
    name = "https/tls13"
    port = None
    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS_1_3

    def __init__(self, *args, **kwargs):
        super(TLSv13Transform, self).__init__(*args, **kwargs)

    def _transform_object(self, obj):
        zout = ZMapTransformOutput()
        tempout = dict()
        wrapped = Transformable(obj)
        error_component = wrapped['error_component'].resolve()
        if error_component is not None and error_component == 'connect':
            raise errors.IgnoreObject("Error connecting")
        tls_handshake = wrapped['data']['tls']
        value = tls_handshake['server_hello']['version']['value'].resolve()
        out = dict()
        if value is not None:
            version = int(value)
            out['support'] = True if version == 772 else False
        else:
            raise errors.IgnoreObject("Empty output dict")

        zout.transformed = out
        return zout


class DHETransform(ZGrabTransform):
    name = "https/dhe"
    port = None
    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.DHE

    def __init__(self, *args, **kwargs):
        super(DHETransform, self).__init__(*args, **kwargs)

    def _transform_object(self, obj):

        zout = ZMapTransformOutput()
        out = dict()
        wrapped = Transformable(obj)
        error_component = wrapped['error_component'].resolve()
        if error_component is not None and error_component == 'connect':
            raise errors.IgnoreObject("Error connecting")
        dh = wrapped['data']['tls']['server_key_exchange']['dh_params']
        dh_prime_value = dh['prime']['value'].resolve()
        dh_prime_length = dh['prime']['length'].resolve()
        dh_generator_value = dh['generator']['value'].resolve()
        dh_generator_length = dh['generator']['length'].resolve()

        if dh_prime_value or dh_generator_value is not None:
            out['dh_params'] = dict()
        if dh_prime_value is not None:
            out['dh_params']['prime'] = dict()
        if dh_generator_value is not None:
            out['dh_params']['generator'] = dict()
        if dh_prime_value is not None:
            out['dh_params']['prime']['value'] = dh_prime_value
        if dh_prime_length is not None:
            out['dh_params']['prime']['length'] = dh_prime_length
        if dh_generator_value is not None:
            out['dh_params']['generator']['value'] = dh_generator_value
        if dh_generator_length is not None:
            out['dh_params']['generator']['length'] = dh_generator_length

        out["support"] = bool(out)

        zout.transformed = out
        return zout


class DHEExportTransform(ZGrabTransform):
    name = "https/dhe"
    port = None
    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.DHE_EXPORT

    def __init__(self, *args, **kwargs):
        super(DHEExportTransform, self).__init__(*args, **kwargs)

    def _transform_object(self, obj):

        zout = ZMapTransformOutput()
        out = dict()
        wrapped = Transformable(obj)
        error_component = wrapped['error_component'].resolve()
        if error_component is not None and error_component == 'connect':
            raise errors.IgnoreObject("Error connecting")
        dh = wrapped['data']['tls']['server_key_exchange']['dh_params']
        dh_prime_value = dh['prime']['value'].resolve()
        dh_prime_length = dh['prime']['length'].resolve()
        dh_generator_value = dh['generator']['value'].resolve()
        dh_generator_length = dh['generator']['length'].resolve()

        if dh_prime_value or dh_generator_value is not None:
            out['dh_params'] = dict()
        if dh_prime_value is not None:
            out['dh_params']['prime'] = dict()
        if dh_generator_value is not None:
            out['dh_params']['generator'] = dict()
        if dh_prime_value is not None:
            out['dh_params']['prime']['value'] = dh_prime_value
        if dh_prime_length is not None:
            out['dh_params']['prime']['length'] = dh_prime_length
        if dh_generator_value is not None:
            out['dh_params']['generator']['value'] = dh_generator_value
        if dh_generator_length is not None:
            out['dh_params']['generator']['length'] = dh_generator_length

        out["support"] = bool(out)

        zout.transformed = out
        return zout


class ECDHETransform(ZGrabTransform):
    name = "https/ecdhe"
    port = None
    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.ECDHE

    def __init__(self, *args, **kwargs):
        super(ECDHETransform, self).__init__(*args, **kwargs)

    def _transform_object(self, obj):

        zout = ZMapTransformOutput()
        out = dict()
        wrapped = Transformable(obj)
        error_component = wrapped['error_component'].resolve()
        if error_component is not None and error_component == 'connect':
            raise errors.IgnoreObject("Error connecting")
        ecdh = wrapped['data']['tls']['server_key_exchange']['ecdh_params']['curve_id']

        ecdh_name = ecdh['name'].resolve()
        ecdh_id = ecdh['id'].resolve()

        if ecdh_name or ecdh_id is not None:
            out['ecdh_params'] = dict()
            out['ecdh_params']['curve_id'] = dict()
        if ecdh_name is not None:
            out['ecdh_params']['curve_id']['name'] = ecdh_name
        if ecdh_id is not None:
            out['ecdh_params']['curve_id']['id'] = ecdh_id

        out["support"] = bool(out)


        zout.transformed = out
        return zout


class RSAExportTransform(ZGrabTransform):
    name = "https/rsa"
    port = None
    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.RSA_EXPORT

    def __init__(self, *args, **kwargs):
        super(RSAExportTransform, self).__init__(*args, **kwargs)

    def _transform_object(self, obj):

        zout = ZMapTransformOutput()
        out = dict()
        wrapped = Transformable(obj)
        error_component = wrapped['error_component'].resolve()
        if error_component is not None and error_component == 'connect':
            raise errors.IgnoreObject("Error connecting")
        rsa = wrapped['data']['tls']['server_key_exchange']['rsa_params']
        rsa_exponent = rsa['exponent'].resolve()
        rsa_modulus = rsa['modulus'].resolve()
        rsa_length = rsa['length'].resolve()

        if rsa_exponent or rsa_modulus is not None:
            out['rsa_params'] = dict()
        if rsa_exponent is not None:
            out['rsa_params']['exponent'] = rsa_exponent
        if rsa_modulus is not None:
            out['rsa_params']['modulus'] = rsa_modulus
        if rsa_length is not None:
            out['rsa_params']['length'] = rsa_length

        out["support"] = bool(out)

        zout.transformed = out
        return zout


class ExtendedRandomTransform(ZGrabTransform):

        name = "https/extended_random"
        port = None
        protocol = protocols.HTTPS
        subprotocol = protocols.HTTPS.EXTENDED_RANDOM

        def __init__(self, *args, **kwargs):
            super(ExtendedRandomTransform, self).__init__(*args, **kwargs)

        def _transform_object(self, obj):
            zout = ZMapTransformOutput()
            out = dict()
            wrapped = Transformable(obj)
            error_component = wrapped['error_component'].resolve()
            if error_component is not None and error_component == 'connect':
                raise errors.IgnoreObject("Error connecting")
            server_hello = wrapped['data']['tls']['server_hello']
            if server_hello.resolve() is None:
                raise IgnoreObject("missing server hello")
            exr = server_hello['extended_random'].resolve()
            if exr is not None:
                out['extended_random_support'] = True
            else:
                out['extended_random_support'] = False
            zout.transformed = out
            return zout
