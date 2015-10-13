from ztag.transform import ZMapTransform, ZGrabTransform
from ztag import protocols


class RSAExportTransform(ZGrabTransform):

    name = "https/rsa_export"
    port = None
    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.RSA_EXPORT

    def __init__(self, *args, **kwargs):
        super(RSAExportTransform, self).__init__(*args, **kwargs)

    def _transform_object(self, d):
        tls = d['log'][1]['data']
        server_hello = tls['server_hello']
        out_params = dict()
        try:
            params = tls['rsa_export_params']
            out_params['modulus'] = params['modulus']
            out_params['exponent'] = params['exponent']
        except (KeyError, TypeError, IndexError):
            pass
        cipher_suite = server_hello['cipher_suite']
        out = {
            'cipher_suite': cipher_suite,
            'rsa_key_exchange': out_params,
            'ip_address': d['host'],
            'timestamp': d['time'],
        }
        return out


class DHETransform(ZGrabTransform):

    name = "https/dhe"
    port = None
    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.DHE

    def __init__(self, *args, **kwargs):
        super(DHETransform, self).__init__(*args, **kwargs)

    def _transform_object(self, d):
        tls = d['log'][1]['data']
        server_hello = tls['server_hello']
        out_params = dict()
        try:
            params = tls['dh_params']
            out_params['p'] = params['prime']
            out_params['bits'] = params['prime_length']
            out_params['g'] = params['generator']
            out_params['y'] = params['public_exponent']
        except (KeyError, TypeError, IndexError):
            pass
        cipher_suite = server_hello['cipher_suite']
        out = {
            'cipher_suite': cipher_suite,
            'params': out_params,
            'ip_address': d['host'],
            'timestamp': d['time'],
        }
        return out


class DHEExportTransform(ZGrabTransform):

    name = "https/dhe_export"
    port = None
    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.DHE_EXPORT

    def __init__(self, *args, **kwargs):
        super(DHEExportTransform, self).__init__(*args, **kwargs)

    def _transform_object(self, d):
        tls = d['log'][1]['data']
        server_hello = tls['server_hello']
        out_params = dict()
        try:
            params = tls['dh_export_params']
            out_params['p'] = params['prime']
            out_params['bits'] = params['prime_length']
            out_params['g'] = params['generator']
            out_params['y'] = params['public_exponent']
        except (KeyError, TypeError, IndexError):
            pass
        cipher_suite = server_hello['cipher_suite']
        out = {
            'cipher_suite': cipher_suite,
            'params': out_params,
            'ip_address': d['host'],
            'timestamp': d['time'],
        }
        return out
