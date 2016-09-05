from ztag.transform import Transformable

def make_tls_obj(tls):
    out = dict()
    wrapped = Transformable(tls)
    error_component = wrapped['error_component'].resolve()
    if error_component != None and error_component == 'connect':
        raise errors.IgnoreObject("Error connecting")
    certificates = []
    hello = wrapped['server_hello']
    server_certificates = wrapped['server_certificates']
    cipher_suite = hello['cipher_suite']
    validation = server_certificates['validation']
    server_key_exchange = wrapped['server_key_exchange']
    ecdh = server_key_exchange['ecdh_params']['curve_id']
    dh = server_key_exchange['dh_params']
    rsa = server_key_exchange['rsa_params']
    signature = server_key_exchange['signature']
    signature_hash = signature['signature_and_hash_type']

    version = hello['version']['name'].resolve()

    if version != None:
        out['version'] = version

    cipher_id = cipher_suite['hex'].resolve()
    cipher_name = cipher_suite['name'].resolve()
    ocsp_stapling = hello['ocsp_stapling'].resolve()
    secure_renegotiation = hello['secure_renegotiation'].resolve()

    if cipher_id or cipher_name != None:
        out['cipher_suite'] = dict()
    if cipher_id != None:
        out['cipher_suite']['id'] = cipher_id
    if cipher_name != None:
        out['cipher_suite']['name'] = cipher_name
    if ocsp_stapling != None:
        out['ocsp_stapling'] = ocsp_stapling

    cert = server_certificates['certificate'].resolve()
    if cert != None:
        out['certificate'] = {
            'parsed': cert['parsed'],
        }
        certificates.append(cert)

    chain = wrapped['server_certificates']['chain'].resolve()
    if chain != None:
        out['chain'] = [
            {'parsed': c['parsed']} for c in chain
        ]
        cert['parents'] = list()
        for c in chain:
            certificates.append(c)
            cert['parents'].append(c['parsed']['fingerprint_sha256'])

    browser_trusted = validation['browser_trusted'].resolve()
    browser_error = validation['browser_error'].resolve()
    matches_domain = validation['matches_domain'].resolve()

    if browser_trusted or browser_error or matches_domain != None:
        out['validation'] = dict()
    if browser_trusted != None:
        out['validation']['browser_trusted'] = browser_trusted
        cert['nss_trusted'] = browser_trusted
    if browser_error != None:
        out['validation']['browser_error'] = browser_error
    if matches_domain != None:
        out['validation']['matches_domain'] = matches_domain

    ecdh_name = ecdh['name'].resolve()
    ecdh_id = ecdh['id'].resolve()
    dh_prime_value = dh['prime']['value'].resolve()
    dh_prime_length = dh['prime']['length'].resolve()
    dh_generator_value = dh['generator']['value'].resolve()
    dh_generator_length = dh['generator']['length'].resolve()
    rsa_exponent = rsa['exponent'].resolve()
    rsa_modulus = rsa['modulus'].resolve()
    rsa_length = rsa['length'].resolve()
    ecdh_name = ecdh['name'].resolve()
    ecdh_id = ecdh['id'].resolve()

    if ecdh_name or dh_prime_value or dh_generator_value or rsa_exponent != None:
        out['server_key_exchange'] = dict()

    if ecdh_name or ecdh_id != None:
        out['server_key_exchange']['ecdh_params'] = dict()
        out['server_key_exchange']['ecdh_params']['curve_id'] = dict()
    if ecdh_name != None:
        out['server_key_exchange']['ecdh_params']['curve_id']['name'] = ecdh_name
    if ecdh_id != None:
        out['server_key_exchange']['ecdh_params']['curve_id']['id'] = ecdh_id

    if dh_prime_value or dh_generator_value != None:
        out['server_key_exchange']['dh_params'] = dict()
    if dh_prime_value != None:
        out['server_key_exchange']['dh_params']['prime'] = dict()
    if dh_generator_value != None:
        out['server_key_exchange']['dh_params']['generator'] = dict()
    if dh_prime_value != None:
        out['server_key_exchange']['dh_params']['prime']['value'] = dh_prime_value
    if dh_prime_length != None:
        out['server_key_exchange']['dh_params']['prime']['length'] = dh_prime_length
    if dh_generator_value != None:
        out['server_key_exchange']['dh_params']['generator']['value'] = dh_generator_value
    if dh_generator_length != None:
        out['server_key_exchange']['dh_params']['generator']['length'] = dh_generator_length

    if rsa_exponent or rsa_modulus != None:
        out['server_key_exchange']['rsa_params'] = dict()
    if rsa_exponent != None:
        out['server_key_exchange']['rsa_params']['exponent'] = rsa_exponent
    if rsa_modulus != None:
        out['server_key_exchange']['rsa_params']['modulus'] = rsa_modulus
    if rsa_length != None:
        out['server_key_exchange']['rsa_params']['length'] = rsa_length

    signature_valid = signature['valid'].resolve()
    signature_error = signature['signature_error'].resolve()
    signature_algorithm = signature_hash['signature_algorithm'].resolve()
    signature_hash = signature_hash['hash_algorithm'].resolve()

    if signature_valid or signature_error != None:
        out['signature'] = dict()
    if signature_valid != None:
        out['signature']['valid'] = signature_valid
    if signature_error != None:
        out['signature']['signature_error'] = signature_error
    if signature_algorithm != None:
        out['signature']['signature_algorithm'] = signature_algorithm
    if signature_hash != None:
        out['signature']['hash_algorithm'] = signature_hash

    if len(out) == 0:
        raise errors.IgnoreObject("Empty output dict")

    return out, certificates
