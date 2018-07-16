from zschema.leaves import *
from zschema.compounds import *

import zschema.registry

from ztag.annotation import Annotation

import zcrypto_schemas.zcrypto as zcrypto
import zgrab2_schemas.zgrab2 as zgrab2
import zgrab2_schemas.zgrab2.mssql as zgrab2_mssql
import zgrab2_schemas.zgrab2.oracle as zgrab2_oracle
import zgrab2_schemas.zgrab2.ssh as zgrab2_ssh

class CensysString(WhitespaceAnalyzedString):
    "default type for any strings in Censys"
    ES_INCLUDE_RAW = True


def remove_strings(schema):
    out = _remove_strings(schema)
    return out

def _recurse_object(v):
    # Attempt to retain attributes (required/doc/etc)
    from copy import deepcopy

    if type(v) == zschema.leaves.String:
        # TODO; Find the right way to copy over all of v's attributes but just
        # change its type to a CensysString()
        return CensysString()
    elif isinstance(v, ListOf):
        out = deepcopy(v)
        out.object_ =_recurse_object(v.object_)
        return out
    elif isinstance(v, SubRecord):
        return _remove_strings(v)
    return v


def _remove_strings(schema):
    if not isinstance(schema, SubRecord):
        return schema
    out = schema.new()
    for k, v in schema.definition.iteritems():
        out.definition[k] = _recurse_object(v)
    return out



__local_metadata = {}
for key in Annotation.LOCAL_METADATA_KEYS:
    __local_metadata[key] = CensysString()
local_metadata = SubRecord(__local_metadata, type_name="local_metadata")

# The probe_* types roughly correspond to individual probe connections
# with the target service (or, in old-sytle ZGrab, a single grab with
# particular parameters).  Some may occasionally fail to be populated
# due to intermittent network problems.

probe_tls_dh_export_type = SubRecordType({
    "dh_params": zcrypto.DHParams(doc="The parameters for the key."),
    "support": Boolean(),
    "metadata": local_metadata,
    "timestamp": Timestamp(),
}, type_name="probe_tls_dh_export")

probe_tls_dh_type = SubRecordType({
    "dh_params": zcrypto.DHParams(doc="The parameters for the key."),
    "support": Boolean(),
    "metadata": local_metadata,
    "timestamp": Timestamp(),
}, type_name="probe_tls_dh")

probe_tls_rsa_export_type = SubRecordType({
    "rsa_params":zcrypto.RSAPublicKey(),
    "support":Boolean(),
    "metadata":local_metadata,
    "timestamp":Timestamp(),
}, type_name="probe_tls_rsa_export")

probe_tls_ecdh_type = SubRecordType({
    "ecdh_params":zcrypto.ECDHParams(),
    "support":Boolean(),
    "metadata":local_metadata,
    "timestamp":Timestamp(),
}, type_name="probe_tls_ecdh")

certificate_trust_type = SubRecordType({
    "type":Enum(doc="root, intermediate, or leaf certificate"),
    "trusted_path":Boolean(doc="Does certificate chain up to browser root store"),
    "valid":Boolean(doc="is this certificate currently valid in this browser"),
    "was_valid":Boolean(doc="was this certificate ever valid in this browser")
}, type_name="certificate_trust")

_zcrypto_parsed_cert = zcrypto.ParsedCertificate()

certificate_type = SubRecordType({
    "parsed": SubRecord({
        "__expanded_names": ListOf(CensysString()),
    }, extends=_zcrypto_parsed_cert),
    "validation":SubRecord({
        "nss":certificate_trust_type(category="NSS (Firefox) Validation"),
        "apple":certificate_trust_type(category="Apple Validation"),
        "microsoft":certificate_trust_type(category="Microsoft Validation"),
        "android":certificate_trust_type(),
        "java":certificate_trust_type(),
    }),
}, type_name="certificate")


server_certificate_valid = SubRecord({
    "complete_chain":Boolean(doc="does server provide a chain up to a root"),
    "valid":Boolean(doc="is this certificate currently valid in this browser"),
    "error":CensysString()
})

probe_tls_type = SubRecordType({
    # This is server_hello.version.name
    "version": zcrypto.TLSVersionName(),
    # cipher_suite = { id: server_hello.cipher_suite.hex, name: server_hello.cipher_suite.name }
    "cipher_suite": SubRecord({
        "id": String(doc="The hexadecimal string representation of the numeric cipher algorithm identifier."),
        "name": CensysString(
            doc="The algorithm identifier for the cipher algorithm identifier, see e.g. https://www.iana.org/assignments/tls-parameters/tls-parameters.xhtml.",
            examples=["unknown", "TLS_RSA_WITH_RC4_128_MD5", "TLS_KRB5_WITH_3DES_EDE_CBC_SHA", "TLS_ECDHE_PSK_WITH_AES_128_GCM_SHA256"],
        ),
    }),
    # server_hello.ocsp_stapling
    "ocsp_stapling": Boolean(),
    # server_hello.secure_renegotiation
    "secure_renegotiation": Boolean(),
    # certificate.parsed = server_certificates.certificate.parsed
    "certificate": certificate_type(),
    # chain.parsed = [ elt.parsed for elt in server_certificates.chain ]
    "chain": ListOf(certificate_type()),
    # server_hello.scts
    "scts": ListOf(zcrypto.SCTRecord()),
    # session_ticket = { key: session_ticket[key] for key in ("length, "lifetime_hint") }
    "session_ticket": zcrypto.SessionTicket(),
    # validation = { server_certificates.validation[key] for key in ("browser_trusted", "browser_error", "matches_domain") }
    "validation": zcrypto.TLSCertificateValidation(),
    # server_key_exchange = { server_key_exchange[key] for key in ("ecdh_params", "dh_params", "rsa_params")
    "server_key_exchange": zcrypto.ServerKeyExchange(),
    # signature = ...
    "signature": SubRecord({
        # ... = signature.valid
        "valid": Boolean(),
        # ... = signature.signature_error
        "signature_error": CensysString(),
        # ... = signature.signature_and_hash_type.signature_algorithm
        "signature_algorithm": String(),
        # ... = signature.signature_and_hash_type.hash_algorithm
        "hash_algorithm": String(),
    }),
    "metadata": local_metadata,
    "timestamp": Timestamp(),
}, type_name = "probe_tls")

probe_tls = probe_tls_type()

probe_tls_sslv2_type = SubRecordType({
    "support": Boolean(),
    "extra_clear": Boolean(),
    "export": Boolean(),
    "certificate": certificate_type(),
    "ciphers": ListOf(SubRecord({
        "name": String(),
        "id": Unsigned32BitInteger(),
    })),
    "metadata": local_metadata,
    "timestamp":Timestamp(),
}, type_name="probe_tls_sslv2")

probe_tls_heartbleed_type = SubRecordType({
    "heartbeat_enabled":Boolean(),
    "heartbleed_vulnerable":Boolean(),
    "metadata":local_metadata,
    "timestamp":Timestamp(),
}, type_name="probe_tls_heartbleed")

probe_tls_extended_random_type = SubRecordType({
    "extended_random_support": Boolean(),
    "metadata":local_metadata,
    "timestamp":Timestamp(),
}, type_name="probe_tls_extended_random")

probe_smtp_starttls_banner_type = SubRecordType({
    "banner": CensysString(),
    "ehlo": CensysString(),
    "starttls": CensysString(),
    "tls": probe_tls_type(),
    "metadata":local_metadata,
    "timestamp":Timestamp(),
}, type_name = "probe_smtp_startls_banner")

probe_mail_starttls_banner_type = SubRecordType({
    "banner": CensysString(),
    "starttls": CensysString(),
    "tls": probe_tls_type(),
    "metadata": local_metadata,
    "timestamp":Timestamp(),
}, type_name = "probe_mail_starttls_banner")

probe_mail_tls_banner_type = SubRecordType({
    "tls": probe_tls_type(),
    "banner": CensysString(),
    "metadata":local_metadata,
    "timestamp":Timestamp(),
}, type_name="probe_mail_tls_banner")

http_unknown_header_type = SubRecordType({
    "key":String(),
    "value":CensysString()
})

http_headers_type = SubRecordType({
    "access_control_allow_origin":CensysString(),
    "accept_patch":CensysString(),
    "accept_ranges":CensysString(),
    "age":CensysString(),
    "allow":CensysString(),
    "alt_svc":CensysString(),
    "alternate_protocol":CensysString(),
    "cache_control":CensysString(),
    "connection":CensysString(),
    "content_disposition":CensysString(),
    "content_encoding":CensysString(),
    "content_language":CensysString(),
    "content_length":CensysString(),
    "content_location":CensysString(),
    "content_md5":CensysString(),
    "content_range":CensysString(),
    "content_type":CensysString(),
    "date":CensysString(),
    "etag":CensysString(),
    "expires":CensysString(),
    "last_modified":CensysString(),
    "link":CensysString(),
    "location":CensysString(),
    "p3p":CensysString(),
    "pragma":CensysString(),
    "proxy_authenticate":CensysString(),
    "public_key_pins":CensysString(),
    "refresh":CensysString(),
    # Currently misindexed in IPv4 schema
    #"referer":CensysString(),
    "retry_after":CensysString(),
    "server":CensysString(),
    "set_cookie":CensysString(),
    "status":CensysString(),
    "strict_transport_security":CensysString(),
    "trailer":CensysString(),
    "transfer_encoding":CensysString(),
    "upgrade":CensysString(),
    "vary":CensysString(),
    "via":CensysString(),
    "warning":CensysString(),
    "www_authenticate":CensysString(),
    "x_frame_options":CensysString(),
    "x_xss_protection":CensysString(),
    "content_security_policy":CensysString(),
    "x_content_security_policy":CensysString(),
    "x_webkit_csp":CensysString(),
    "x_content_type_options":CensysString(),
    "x_powered_by":CensysString(),
    "x_ua_compatible":CensysString(),
    "x_content_duration":CensysString(),
    "x_forwarded_for":CensysString(),
    "proxy_agent":CensysString(),
    "unknown":ListOf(http_unknown_header_type())
}, type_name="http_headers")

probe_http_request_type = SubRecordType({
    "status_code":Unsigned16BitInteger(),
    "status_line":CensysString(),
    "body":HTML(),
    "headers":http_headers_type(),
    "body_sha256":HexString(validation_policy="warn"),
    "title":CensysString(),
    "metadata":local_metadata,
    "timestamp":Timestamp(),
}, type_name="probe_http_request")

# golang_crypto_param = SubRecord({
#     "value":IndexedBinary(),
#     "length":Unsigned32BitInteger()
# })

#ztag_open_proxy = SubRecord({
#    "connect":SubRecord({
#      "status_code":Integer(),
#      "status_line":CensysString(),
#      "body":CensysString(),
#      "headers":http_headers_type()
#    }),
#    "get":SubRecord({
#      "status_code":Integer(),
#      "status_line":CensysString(),
#      "body":CensysString(),
#      "headers":http_headers_type(),
#      "random_present":Boolean(),
#      "body_sha256":HexString()
#    }),
#    "metadata":local_metadata
#})

probe_ssh_v2_type = SubRecordType({
    "metadata": local_metadata,
    "timestamp": Timestamp(),
    "banner": zgrab2_ssh.AnalyzedEndpointID(),
    # This is a massaged version of zgrab2_ssh.KexInitMessage
    "support": SubRecord({
        "kex_algorithms": zgrab2_ssh.KexAlgorithms(),
        "host_key_algorithms": zgrab2_ssh.KeyAlgorithms(),
        "first_kex_follows": Boolean(),
        "client_to_server": SubRecord({
            "ciphers": zgrab2_ssh.CipherAlgorithms(),
            "macs": zgrab2_ssh.MACAlgorithms(),
            "compressions": zgrab2_ssh.CompressionAlgorithms(),
            "languages": zgrab2_ssh.LanguageTags(),
        }),
        "server_to_client":SubRecord({
            "ciphers": zgrab2_ssh.CipherAlgorithms(),
            "macs": zgrab2_ssh.MACAlgorithms(),
            "compressions": zgrab2_ssh.CompressionAlgorithms(),
            "languages": zgrab2_ssh.LanguageTags(),
        }),
    }),
    # This is a massaged version of zgrab2_ssh.AlgorithmSelection
    "selected": SubRecord({
        "kex_algorithm": zgrab2_ssh.KexAlgorithm(),
        "host_key_algorithm": zgrab2_ssh.KeyAlgorithm(),
        "client_to_server": zgrab2_ssh.DirectionAlgorithms(),
        "server_to_client": zgrab2_ssh.DirectionAlgorithms(),
    }),
    "key_exchange": zgrab2_ssh.KeyExchange(),
    # This is a massaged version of zgrab2_ssh.SSHPublicKeyCert
    "server_host_key": SubRecord({
        "key_algorithm": zgrab2_ssh.KeyAlgorithm(),
        "fingerprint_sha256": HexString(),
        "rsa_public_key": zcrypto.RSAPublicKey(),
        "dsa_public_key": zcrypto.DSAPublicKey(),
        "ecdsa_public_key": zcrypto.ECDSAPublicKey(),
        "ed25519_public_key": zgrab2_ssh.ED25519PublicKey(),
        "certkey_public_key": SubRecord({
            # "nonce" is an IndexedBinary here, not a Binary()
            "nonce": IndexedBinary(),
            # This is an SSHPublicKey ("algorithm", not "key_algorithm")
            "key": zgrab2_ssh.SSHPublicKey(),
            "serial": String(),
            # "cert_type" is renamed to "type"
            "type": zgrab2_ssh.CertType(exclude=["bigquery"]),
            "key_id": String(),
            "valid_principals": ListOf(String()),
            "validity": SubRecord({
                # These are DateTimes in SSHPublicKeyCert
                "valid_after": Timestamp(doc="Timestamp of when certificate is first valid. Timezone is UTC."),
                "valid_before": Timestamp(doc="Timestamp of when certificate expires. Timezone is UTC."),
                "length": Signed64BitInteger(),
            }),
            # "reserved": Binary(),
            "signature_key": SubRecord({
                "key_algorithm": zgrab2_ssh.KeyAlgorithm(),
                "fingerprint_sha256": HexString(),
                "rsa_public_key": zcrypto.RSAPublicKey(),
                "dsa_public_key": zcrypto.DSAPublicKey(),
                "ecdsa_public_key": zcrypto.ECDSAPublicKey(),
                "ed25519_public_key": zgrab2_ssh.ED25519PublicKey(),
            }),
            "signature": SubRecord({
                "signature_algorithm": SubRecord({
                    "name": zgrab2_ssh.KeyAlgorithm(),
                }),
                "value": IndexedBinary(),
            }),
            "parse_error": String(),
            # Flattens known/unknown
            "extensions":SubRecord({
                "permit_X11_forwarding": Boolean(),
                "permit_agent_forwarding": Boolean(),
                "permit_port_forwarding": Boolean(),
                "permit_pty": Boolean(),
                "permit_user_rc": Boolean(),
                "unknown": ListOf(String()),
            }),
            # Flattens known/unknown
            "critical_options": SubRecord({
                "force_command": Boolean(),
                "source_address": Boolean(),
                "unknown": ListOf(String()),
            }),
        }),
    }),
}, type_name="probe_ssh_v2")

probe_ftp_banner_type = SubRecordType({
    "banner":CensysString(),
    "metadata":local_metadata,
    "timestamp":Timestamp(),
}, type_name="probe_ftp_banner")

telnet_cap_type = SubRecordType({
    "name":String(),
    "value":Unsigned32BitInteger()
}, type_name="telnet_cap")

probe_telnet_banner_type = SubRecordType({
    "support":Boolean(),
    "banner":CensysString(),
    "will": ListOf(telnet_cap_type()),
    "wont": ListOf(telnet_cap_type()),
    "do": ListOf(telnet_cap_type()),
    "dont": ListOf(telnet_cap_type()),
    "metadata":local_metadata,
    "timestamp":Timestamp(),
}, type_name="probe_telnet_banner")

probe_modbus_device_id_type = SubRecordType({
    "support":Boolean(),
    "function_code":Unsigned16BitInteger(),
    "mei_response":SubRecord({
      "conformity_level":Signed32BitInteger(),
      "objects":SubRecord({
        "vendor":CensysString(),
        "product_code":CensysString(),
        "revision":CensysString(),
        "vendor_url":URL(),
        "product_name":CensysString(),
        "model_name":CensysString(),
        "user_application_name":CensysString(),
      })
    }),
    "metadata":local_metadata,
    "timestamp":Timestamp(),
}, type_name="probe_modbus_device_id")

probe_bacnet_device_id_type = SubRecordType({
    "support":Boolean(),
    "instance_number": Signed32BitInteger(),
    "vendor": SubRecord({
        "id": Signed32BitInteger(),
        "reported_name":CensysString(),
        "official_name":CensysString(),
    }),
    "firmware_revision": String(),
    "application_software_revision":String(),
    "object_name":CensysString(),
    "model_name":CensysString(),
    "description":CensysString(),
    "location":CensysString(),
    "metadata":local_metadata,
    "timestamp":Timestamp(),
}, type_name="probe_bacnet_device_id")

dns_question_type = SubRecordType({
    "name":String(),
    "type":String()
}, type_name="dns_question")

dns_answer_type = SubRecordType({
    "name":String(),
    "response":CensysString(),
    "type":String()
}, type_name="dns_answer")

probe_dns_lookup_type = SubRecordType({
    "support":Boolean(),
    "errors":Boolean(),
    "open_resolver":Boolean(),
    "resolves_correctly":Boolean(),
    "answers":ListOf(dns_answer_type()),
    "authorities":ListOf(dns_answer_type()),
    "additionals":ListOf(dns_answer_type()),
    "questions":ListOf(dns_question_type()),
    "metadata":local_metadata,
    "timestamp":Timestamp(),
}, type_name="probe_dns_lookup")

probe_tls_support_type = SubRecordType({
    "support": Boolean(),
    "metadata":local_metadata,
    "timestamp":Timestamp(),
}, type_name="probe_tls_support")

probe_fox_device_id_type = SubRecordType({
    "support":Boolean(),
    "version":CensysString(),
    "id":Signed32BitInteger(),
    "hostname":CensysString(),
    "host_address":CensysString(),
    "app_name":CensysString(),
    "app_version":CensysString(),
    "vm_name":CensysString(),
    "vm_version":CensysString(),
    "os_name":CensysString(),
    "os_version":CensysString(),
    "station_name":CensysString(),
    "language":CensysString(),
    "time_zone":CensysString(),
    "host_id":CensysString(),
    "vm_uuid":CensysString(),
    "brand_id":CensysString(),
    "sys_info":CensysString(),
    "auth_agent_type":String(),
    "metadata":local_metadata,
    "timestamp":Timestamp(),
}, type_name="probe_fox_device_id")

probe_dnp3_status_type = SubRecordType({
    "support":Boolean(),
    "raw_response":Binary(),
    "metadata":local_metadata,
    "timestamp":Timestamp(),
}, type_name="probe_dnp3_status")

probe_s7_szl_type = SubRecordType({
    "support":Boolean(),
    "system":CensysString(),
    "module":CensysString(),
    "plant_id":CensysString(),
    "copyright":CensysString(),
    "serial_number":CensysString(),
    "reserved_for_os":CensysString(),
    "module_type":CensysString(),
    "memory_serial_number":CensysString(),
    "cpu_profile":CensysString(),
    "oem_id":CensysString(),
    "location":CensysString(),
    "module_id":CensysString(),
    "hardware":CensysString(),
    "firmware":CensysString(),
    "metadata":local_metadata,
    "timestamp":Timestamp(),
}, type_name = "probe_s7_szl")

probe_smb_banner_type = SubRecordType({
    "smbv1_support":Boolean(),
    "metadata":local_metadata,
}, type_name = "smb_banner")

probe_upnp_discovery_type = SubRecordType({
    "usn": String(),
    "agent": String(),
    "st": String(),
    "ext": String(),
    "location": String(),
    "server": String(),
    "cache_control": String(),
    "x_user_agent": String(),
    "metadata": local_metadata,
}, type_name = "probe_upnp_discovery")

# Add the common zgrab2 fields to the results schema which are added by
# ZGrab2Transform._transform_object().
def ztag_zgrab2_transformed(service, results):
    results["supported"] = Boolean(doc="If true, %s was detected on this machine." % service)
    results["metadata"] = local_metadata
    return results

# The oracle ztag transform is a plain copy of the "handshake" field.
ztag_oracle = ztag_zgrab2_transformed(service="Oracle", results=zgrab2_oracle.oracle_scan_response["result"]["handshake"] | remove_strings)

ztag_oracle["tls"] = probe_tls_type(doc="The TLS handshake with the server (if applicable).")

ztag_mssql = ztag_zgrab2_transformed(service="MSSQL", results=SubRecord({
    "version": CensysString(doc="The MSSQL version returned by the server in "
                                "the PRELOGIN response. Its format is "
                                "'MAJOR.MINOR.BUILD_NUMBER'."),
    "instance_name": CensysString(doc="The value of the INSTANCE field "
                                      "returned by the server in the PRELOGIN "
                                      "response."),
    "encrypt_mode": Enum(values=zgrab2_mssql.ENCRYPT_MODES,
                         doc="The negotiated encryption mode for the session. "
                             "See https://msdn.microsoft.com/en-us/library/dd357559.aspx "
                             "for details."),
    "tls": probe_tls_type(doc="The TLS handshake with the server (for "
                             "non-encrypted connections, this used only "
                             "for the authentication phase).")
}))

ztag_mysql = ztag_zgrab2_transformed(service="MySQL", results=SubRecord({
    "protocol_version": zgrab2.mysql.mysql_scan_response["result"]["protocol_version"] | remove_strings,
    "server_version": zgrab2.mysql.mysql_scan_response["result"]["server_version"] | remove_strings,
    "capability_flags": zgrab2.mysql.mysql_capability_flags | remove_strings,
    "status_flags": zgrab2.mysql.mysql_server_status_flags | remove_strings,
    "error_code": zgrab2.mysql.mysql_scan_response["result"]["error_code"] | remove_strings,
    "error_id": zgrab2.mysql.mysql_scan_response["result"]["error_id"] | remove_strings,
    "error_message": zgrab2.mysql.mysql_scan_response["result"]["error_message"] | remove_strings,
    "tls": probe_tls_type(doc="If the server allows upgrading the "
                             "session to use TLS, this is the log of "
                             "the handshake.")
}))

ztag_postgres = ztag_zgrab2_transformed(service="PostgreSQL", results=SubRecord({
    "supported_versions": CensysString(doc="The error string returned by the "
                                           "server in response to a "
                                           "StartupMessage with "
                                           "ProtocolVersion = 0.0"),
    "protocol_error": zgrab2.postgres.postgres_error | remove_strings,
    "startup_error": zgrab2.postgres.postgres_error | remove_strings,
    "is_ssl": Boolean(doc="If the server supports TLS and the session was "
                          "updated to use TLS, this is true."),
    "authentication_mode": zgrab2.postgres.postgres_auth_mode["mode"] | remove_strings,
    "backend_key_data": zgrab2.postgres.postgres_key_data | remove_strings,
    "tls": probe_tls_type(doc="If the server allows upgrading the "
                             "session to use TLS, this is the log of "
                             "the handshake.")
}))

ztag_schemas = [
    ("ztag_https", probe_tls_type()),
    ("ztag_heartbleed", probe_tls_heartbleed_type()),
    ("ztag_smtp_starttls", probe_smtp_starttls_banner_type()),
    ("ztag_imap_starttls", probe_mail_starttls_banner_type()),
    ("ztag_pop3_starttls", probe_mail_starttls_banner_type()),
    ("ztag_imap_tls", probe_mail_tls_banner_type()),
    ("ztag_pop3_tls", probe_mail_tls_banner_type()),
    ("ztag_http", probe_http_request_type()),
    ("ztag_ftp", probe_ftp_banner_type()),
    ("ztag_dh", probe_tls_dh_type()),
    ("ztag_dh_export", probe_tls_dh_export_type()),
    ("ztag_rsa_export", probe_tls_rsa_export_type()),
    ("ztag_ecdh", probe_tls_ecdh_type()),
    ("ztag_sslv2", probe_tls_sslv2_type()),
    ("ztag_sslv3", probe_tls_support_type()),
    ("ztag_tls1", probe_tls_support_type()),
    ("ztag_tls2", probe_tls_support_type()),
    ("ztag_tls3", probe_tls_support_type()),
    ("ztag_modbus", probe_modbus_device_id_type()),
    ("ztag_extended_random", probe_tls_extended_random_type()),
    ("ztag_ssh_v2", probe_ssh_v2_type()),
    ("ztag_dns_lookup", probe_dns_lookup_type()),
    ("ztag_bacnet", probe_bacnet_device_id_type()),
    ("ztag_fox", probe_fox_device_id_type()),
    ("ztag_dnp3", probe_dnp3_status_type()),
    ("ztag_s7", probe_s7_szl_type()),
    ("ztag_smb", probe_smb_banner_type()),
    ("ztag_upnp_discovery", probe_upnp_discovery_type()),
    ("ztag_oracle", ztag_oracle),
    ("ztag_mssql", ztag_mssql),
    ("ztag_mysql", ztag_mysql),
    ("ztag_telnet", probe_telnet_banner_type()),
]
for (name, schema) in ztag_schemas:
    x = Record({
        "ip_address":IPAddress(required=True),
        #"timestamp":Timestamp(required=True),
        "tags":ListOf(String()),
        "metadata": SubRecord({}, allow_unknown=True, type_name="metadata"),
    }, extends=schema)
    zschema.registry.register_schema("%s" % name, x)


ztag_lookup_spf = SubRecord({
    "raw":CensysString(),
})

ztag_lookup_dmarc = SubRecord({
    "raw":CensysString(),
    "p":String(),
})

ztag_lookup_axfr = SubRecord({
    "servers":ListOf(SubRecord({
        "name":FQDN(),
        "support":Boolean(),
        "error":CensysString(),
        "records":ListOf(SubRecord({
            "name":FQDN(),
            "type":String(),
            "data":CensysString(),
            "ttl":Unsigned32BitInteger()
        })),
    })),
    "truncated":Boolean(),
    "support":Boolean()
})

_zdb_location_fields = {
    "continent":String(),
    "country":CensysString(),
    "country_code":String(),
    "city":CensysString(),
    "postal_code":String(),
    "timezone":CensysString(),
    "province":CensysString(),
    "latitude":Double(),
    "longitude":Double(),
    "registered_country":CensysString(),
    "registered_country_code":String(),
}

zdb_location = SubRecord(_zdb_location_fields)
zdb_restricted_location = SubRecord(_zdb_location_fields, exclude=["bigquery",])

zdb_as = SubRecord({
    "asn":Unsigned32BitInteger(),
    "description":CensysString(),
    "path":ListOf(Unsigned32BitInteger()),
    "rir":String(),
    "routed_prefix":FQDN(),
    "name":CensysString(),
    "country_code":String(),
    "organization":CensysString(),
})


__metadata = {}
for key in Annotation.GLOBAL_METADATA_KEYS:
    __metadata[key] = CensysString()
zdb_metadata = SubRecord(__metadata, type_name="zdb_metadata")

CTServerStatus = SubRecord({
    "index":Signed64BitInteger(),
    "added_to_ct_at":Timestamp(),
    "ct_to_censys_at":Timestamp(),
    "censys_to_ct_at":Timestamp(),
    "sct":Binary(),
})

CTStatus = SubRecord({
    # Censys (reserved)
    "censys_dev":CTServerStatus,
    "censys":CTServerStatus,
    # Google
    "google_aviator":CTServerStatus,
    "google_pilot":CTServerStatus,
    "google_rocketeer":CTServerStatus,
    "google_submariner":CTServerStatus,
    "google_testtube":CTServerStatus,
    "google_icarus":CTServerStatus,
    "google_skydiver":CTServerStatus,
    "google_daedalus":CTServerStatus,
    # Google Argon
    "google_argon_2017":CTServerStatus,
    "google_argon_2018":CTServerStatus,
    "google_argon_2019":CTServerStatus,
    "google_argon_2020":CTServerStatus,
    "google_argon_2021":CTServerStatus,
    # Cloudflare
    "cloudflare_nimbus_2017":CTServerStatus,
    "cloudflare_nimbus_2018":CTServerStatus,
    "cloudflare_nimbus_2019":CTServerStatus,
    "cloudflare_nimbus_2020":CTServerStatus,
    "cloudflare_nimbus_2021":CTServerStatus,
    # Digicert
    "digicert_ct1":CTServerStatus,
    "digicert_ct2":CTServerStatus,
    # Izenpe
    "izenpe_com_ct":CTServerStatus,
    "izenpe_eus_ct":CTServerStatus,
    # Symantec
    "symantec_ws_ct":CTServerStatus,
    "symantec_ws_vega":CTServerStatus,
    "symantec_ws_sirius":CTServerStatus,
    "symantec_ws_deneb":CTServerStatus,
    # Comodo
    "comodo_dodo":CTServerStatus,
    "comodo_mammoth":CTServerStatus,
    "comodo_sabre":CTServerStatus,
    # Wosign, StartCom, Wotrus
    "wosign_ctlog":CTServerStatus,
    "wosign_ct":CTServerStatus,
    "startssl_ct":CTServerStatus,
    "wotrus_ctlog":CTServerStatus,
    "wotrus_ctlog3":CTServerStatus,
    # GDCA
    "gdca_ct":CTServerStatus,
    "gdca_ctlog":CTServerStatus,
    "gdca_log":CTServerStatus,
    "gdca_log2":CTServerStatus,
    # Venafi
    "venafi_api_ctlog":CTServerStatus,
    "venafi_api_ctlog_gen2":CTServerStatus,
    # Nordu
    "nordu_ct_plausible":CTServerStatus,
    # Let's Encrypt
    "letsencrypt_ct_clicky":CTServerStatus,
    # Other
    "cnnic_ctserver":CTServerStatus,
    "certly_log":CTServerStatus,
    "sheca_ct":CTServerStatus,
    "behind_the_sofa":CTServerStatus,
    "certificatetransparency_cn_ct":CTServerStatus,

})

CertificateAudit = SubRecord({
    "ccadb":SubRecord({
        "current_in_intermediates":Boolean(),
        "was_in_intermediates":Boolean(),
        "owner_name":CensysString(),
        "parent_name":CensysString(),
        "certificate_name":CensysString(),
        "certificate_policy":CensysString(),
        "certification_practice_statement":CensysString(),
        "cp_same_as_parent":CensysString(), # TODO: Boolean
        "audit_same_as_parent":CensysString(), # TODO: Boolean
        "standard_audit":CensysString(),
        "br_audit":CensysString(),
        "auditor":CensysString(),
        "standard_audit_statement_timestamp":Timestamp(),
        "management_assertions_by":CensysString(),
        "comments":EnglishString(es_include_raw=True),
        #"ev_policy_oids":CensysString(), # TODO
        #"approval_bug":CensysString(), # TODO
        #"first_nss_release":CensysString(), # TODO
        #"first_firefox_release":CensysString(), # TODO
        #"ev_audit":CensysString(),
        "current_in_roots":Boolean(),
        "was_in_roots":Boolean(),
        #"test_website_valid":CensysString(), # TODO
        #"mozilla_applied_constraints":CensysString(), #TODO
        #"company_website":CensysString(), # TODO
        #"geographic_focus":CensysString(), # TODO
        #"standard_audit_type":CensysString(), # TODO
     }, category="CCADB Audit")
})

ztag_certificate_validation = SubRecord({
    "valid":Boolean(doc="((has_trusted_path && !revoked && !blacklisted) || whitelisted) && !expired"),
    "was_valid":Boolean(doc="True if the certificate is valid now or was ever valid in the past."),
    "trusted_path":Boolean(doc="True if there exists a path from the certificate to the root store."),
    "had_trusted_path":Boolean(doc="True if now or at some point in the past there existed a path "
                                   "from the certificate to the root store."),
    "blacklisted":Boolean(doc="True if the certificate is explicitly blacklisted by some method than OneCRL/CRLSet. "
                              "For example, a set of certificates revoked by Cloudflare are blacklisted by SPKI hash in Chrome."),
    "whitelisted":Boolean(doc="True if the certificate is explicitly whitelisted, "
                              "e.g. the set of trusted WoSign certificates Apple uses."),
    "type":Enum(["leaf","intermediate","root","unknown"], doc="Indicates if the certificate is a root, intermediate, or leaf."),
    "paths":NestedListOf(HexString(), "path"),
    "in_revocation_set":Boolean(doc="True if the certificate is in the revocation set (e.g. OneCRL) associated with this root store."),
    "parents":ListOf(HexString()),
})

class LintBool(String):

    ES_TYPE = "boolean"

# Lints can have any of the following outputs:
#   - RESERVED [should never happen]
#   - NA [not applicable]
#   - NE [not applicable]
#   - PASS [test success]
#   - INFO [failed for info]
#   - WARN [failed for warn]
#   - FAIL [failed for error]
#   - FATAL [test could not complete because cert is broken]
#   - UNKNOWN [should never occur]
# We don't want to store a string for every lint in elasticsearch because
# our index size would explode. Instead we map these to a string:
# {
#     (reserved, unknown, ne, na, pass) -> null,
#     (notice, warning, fail, fatal) -> true
# }
# For BigQuery, we have more options, so we allow some more information:
# {
#     all map to original value
# }
# This is horrible to schema, so define a custom type
Lints = SubRecord({
    "e_basic_constraints_not_critical":LintBool(pr_index=1),
    "e_ca_common_name_missing":LintBool(pr_index=2),
    "e_ca_country_name_invalid":LintBool(pr_index=3),
    "e_ca_country_name_missing":LintBool(pr_index=4),
    "e_ca_crl_sign_not_set":LintBool(pr_index=5),
    "e_ca_is_ca":LintBool(),
    "e_ca_key_cert_sign_not_set":LintBool(),
    "e_ca_key_usage_missing":LintBool(),
    "e_ca_key_usage_not_critical":LintBool(),
    "e_ca_organization_name_missing":LintBool(),
    "e_ca_subject_field_empty":LintBool(),
    "e_cab_dv_conflicts_with_locality":LintBool(),
    "e_cab_dv_conflicts_with_org":LintBool(),
    "e_cab_dv_conflicts_with_postal":LintBool(),
    "e_cab_dv_conflicts_with_province":LintBool(),
    "e_cab_dv_conflicts_with_street":LintBool(),
    "e_cab_iv_requires_personal_name":LintBool(),
    "e_cab_ov_requires_org":LintBool(),
    "e_cert_contains_unique_identifier":LintBool(),
    "e_cert_extensions_version_not_3":LintBool(),
    "e_cert_policy_iv_requires_country":LintBool(),
    "e_cert_policy_iv_requires_province_or_locality":LintBool(),
    "e_cert_policy_ov_requires_country":LintBool(),
    "e_cert_policy_ov_requires_province_or_locality":LintBool(),
    "e_cert_unique_identifier_version_not_2_or_3":LintBool(),
    "e_distribution_point_incomplete":LintBool(),
    "e_dnsname_bad_character_in_label":LintBool(),
    "e_dnsname_contains_bare_iana_suffix":LintBool(),
    "e_dnsname_empty_label":LintBool(),
    "e_dnsname_hyphen_in_sld":LintBool(),
    "e_dnsname_label_too_long":LintBool(),
    "e_dnsname_left_label_wildcard_correct":LintBool(),
    "e_dnsname_not_valid_tld":LintBool(),
    "e_dnsname_underscore_in_sld":LintBool(),
    "e_dnsname_wildcard_only_in_left_label":LintBool(),
    "e_dsa_correct_order_in_subgroup":LintBool(),
    "e_dsa_improper_modulus_or_divisor_size":LintBool(),
    "e_dsa_params_missing":LintBool(),
    "e_dsa_shorter_than_2048_bits":LintBool(),
    "e_dsa_unique_correct_representation":LintBool(),
    "e_ec_improper_curves":LintBool(),
    "e_ev_business_category_missing":LintBool(),
    "e_ev_country_name_missing":LintBool(),
    "e_ev_locality_name_missing":LintBool(),
    "e_ev_organization_name_missing":LintBool(),
    "e_ev_serial_number_missing":LintBool(),
    "e_ev_valid_time_too_long":LintBool(),
    "e_ext_aia_marked_critical":LintBool(),
    "e_ext_authority_key_identifier_critical":LintBool(),
    "e_ext_authority_key_identifier_missing":LintBool(),
    "e_ext_authority_key_identifier_no_key_identifier":LintBool(),
    "e_ext_cert_policy_disallowed_any_policy_qualifier":LintBool(),
    "e_ext_cert_policy_duplicate":LintBool(),
    "e_ext_cert_policy_explicit_text_ia5_string":LintBool(),
    "e_ext_cert_policy_explicit_text_too_long":LintBool(),
    "e_ext_duplicate_extension":LintBool(),
    "e_ext_freshest_crl_marked_critical":LintBool(),
    "e_ext_ian_dns_not_ia5_string":LintBool(),
    "e_ext_ian_empty_name":LintBool(),
    "e_ext_ian_no_entries":LintBool(),
    "e_ext_ian_rfc822_format_invalid":LintBool(),
    "e_ext_ian_space_dns_name":LintBool(),
    "e_ext_ian_uri_format_invalid":LintBool(),
    "e_ext_ian_uri_host_not_fqdn_or_ip":LintBool(),
    "e_ext_ian_uri_not_ia5":LintBool(),
    "e_ext_ian_uri_relative":LintBool(),
    "e_ext_key_usage_cert_sign_without_ca":LintBool(),
    "e_ext_key_usage_without_bits":LintBool(),
    "e_ext_name_constraints_not_critical":LintBool(),
    "e_ext_name_constraints_not_in_ca":LintBool(),
    "e_ext_policy_constraints_empty":LintBool(),
    "e_ext_policy_constraints_not_critical":LintBool(pr_index=99),
    "e_ext_policy_map_any_policy":LintBool(),
    "e_ext_san_contains_reserved_ip":LintBool(),
    "e_ext_san_directory_name_present":LintBool(),
    "e_ext_san_dns_name_too_long":LintBool(),
    "e_ext_san_dns_not_ia5_string":LintBool(),
    "e_ext_san_edi_party_name_present":LintBool(),
    "e_ext_san_empty_name":LintBool(),
    "e_ext_san_missing":LintBool(),
    "e_ext_san_no_entries":LintBool(),
    "e_ext_san_not_critical_without_subject":LintBool(),
    "e_ext_san_other_name_present":LintBool(),
    "e_ext_san_registered_id_present":LintBool(),
    "e_ext_san_rfc822_format_invalid":LintBool(),
    "e_ext_san_rfc822_name_present":LintBool(),
    "e_ext_san_space_dns_name":LintBool(),
    "e_ext_san_uniform_resource_identifier_present":LintBool(),
    "e_ext_san_uri_format_invalid":LintBool(),
    "e_ext_san_uri_host_not_fqdn_or_ip":LintBool(),
    "e_ext_san_uri_not_ia5":LintBool(),
    "e_ext_san_uri_relative":LintBool(),
    "e_ext_subject_directory_attr_critical":LintBool(),
    "e_ext_subject_key_identifier_critical":LintBool(),
    "e_ext_subject_key_identifier_missing_ca":LintBool(),
    "e_generalized_time_does_not_include_seconds":LintBool(),
    "e_generalized_time_includes_fraction_seconds":LintBool(),
    "e_generalized_time_not_in_zulu":LintBool(),
    "e_ian_bare_wildcard":LintBool(),
    "e_ian_dns_name_includes_null_char":LintBool(),
    "e_ian_dns_name_starts_with_period":LintBool(),
    "e_ian_wildcard_not_first":LintBool(),
    "e_inhibit_any_policy_not_critical":LintBool(),
    "e_international_dns_name_not_nfkc":LintBool(),
    "e_international_dns_name_not_unicode":LintBool(),
    "e_invalid_certificate_version":LintBool(),
    "e_issuer_field_empty":LintBool(),
    "e_name_constraint_empty":LintBool(),
    "e_name_constraint_maximum_not_absent":LintBool(),
    "e_name_constraint_minimum_non_zero":LintBool(),
    "e_old_root_ca_rsa_mod_less_than_2048_bits":LintBool(),
    "e_old_sub_ca_rsa_mod_less_than_1024_bits":LintBool(),
    "e_old_sub_cert_rsa_mod_less_than_1024_bits":LintBool(),
    "e_path_len_constraint_improperly_included":LintBool(),
    "e_path_len_constraint_zero_or_less":LintBool(),
    "e_public_key_type_not_allowed":LintBool(),
    "e_root_ca_extended_key_usage_present":LintBool(),
    "e_root_ca_key_usage_must_be_critical":LintBool(),
    "e_root_ca_key_usage_present":LintBool(),
    "e_rsa_exp_negative":LintBool(),
    "e_rsa_mod_less_than_2048_bits":LintBool(),
    "e_rsa_no_public_key":LintBool(),
    "e_rsa_public_exponent_not_odd":LintBool(),
    "e_rsa_public_exponent_too_small":LintBool(),
    "e_san_bare_wildcard":LintBool(),
    "e_san_dns_name_includes_null_char":LintBool(),
    "e_san_dns_name_starts_with_period":LintBool(),
    "e_san_wildcard_not_first":LintBool(),
    "e_serial_number_longer_than_20_octets":LintBool(),
    "e_serial_number_not_positive":LintBool(),
    "e_signature_algorithm_not_supported":LintBool(),
    "e_sub_ca_aia_does_not_contain_ocsp_url":LintBool(),
    "e_sub_ca_aia_marked_critical":LintBool(),
    "e_sub_ca_aia_missing":LintBool(),
    "e_sub_ca_certificate_policies_missing":LintBool(),
    "e_sub_ca_crl_distribution_points_does_not_contain_url":LintBool(),
    "e_sub_ca_crl_distribution_points_marked_critical":LintBool(),
    "e_sub_ca_crl_distribution_points_missing":LintBool(),
    "e_sub_ca_eku_missing":LintBool(),
    "e_sub_ca_eku_name_constraints":LintBool(),
    "e_sub_ca_must_not_contain_any_policy":LintBool(),
    "e_sub_cert_aia_does_not_contain_ocsp_url":LintBool(),
    "e_sub_cert_aia_marked_critical":LintBool(),
    "e_sub_cert_aia_missing":LintBool(),
    "e_sub_cert_cert_policy_empty":LintBool(),
    "e_sub_cert_certificate_policies_missing":LintBool(),
    "e_sub_cert_country_name_must_appear":LintBool(),
    "e_sub_cert_crl_distribution_points_does_not_contain_url":LintBool(),
    "e_sub_cert_crl_distribution_points_marked_critical":LintBool(),
    "e_sub_cert_eku_missing":LintBool(),
    "e_sub_cert_eku_server_auth_client_auth_missing":LintBool(),
    "e_sub_cert_given_name_surname_contains_correct_policy":LintBool(),
    "e_sub_cert_key_usage_cert_sign_bit_set":LintBool(),
    "e_sub_cert_key_usage_crl_sign_bit_set":LintBool(),
    "e_sub_cert_locality_name_must_appear":LintBool(),
    "e_sub_cert_locality_name_must_not_appear":LintBool(),
    "e_sub_cert_not_is_ca":LintBool(),
    "e_sub_cert_or_sub_ca_using_sha1":LintBool(),
    "e_sub_cert_postal_code_must_not_appear":LintBool(),
    "e_sub_cert_province_must_appear":LintBool(),
    "e_sub_cert_province_must_not_appear":LintBool(),
    "e_sub_cert_street_address_should_not_exist":LintBool(),
    "e_sub_cert_valid_time_too_long":LintBool(),
    "e_subject_common_name_max_length":LintBool(),
    "e_subject_common_name_not_from_san":LintBool(),
    "e_subject_contains_noninformational_value":LintBool(),
    "e_subject_contains_reserved_ip":LintBool(),
    "e_subject_country_not_iso":LintBool(),
    "e_subject_empty_without_san":LintBool(),
    "e_subject_info_access_marked_critical":LintBool(),
    "e_subject_locality_name_max_length":LintBool(),
    "e_subject_not_dn":LintBool(),
    "e_subject_organization_name_max_length":LintBool(),
    "e_subject_organizational_unit_name_max_length":LintBool(),
    "e_subject_state_name_max_length":LintBool(),
    "e_utc_time_does_not_include_seconds":LintBool(),
    "e_utc_time_not_in_zulu":LintBool(),
    "e_validity_time_not_positive":LintBool(),
    "e_wrong_time_format_pre2050":LintBool(),
    "n_ca_digital_signature_not_set":LintBool(),
    "n_contains_redacted_dnsname":LintBool(),
    "n_sub_ca_eku_not_technically_constrained":LintBool(),
    "n_subject_common_name_included":LintBool(),
    "w_distribution_point_missing_ldap_or_uri":LintBool(),
    "w_dnsname_underscore_in_trd":LintBool(),
    "w_dnsname_wildcard_left_of_public_suffix":LintBool(),
    "w_eku_critical_improperly":LintBool(),
    "w_ext_aia_access_location_missing":LintBool(),
    "w_ext_cert_policy_contains_noticeref":LintBool(),
    "w_ext_cert_policy_explicit_text_includes_control":LintBool(),
    "w_ext_cert_policy_explicit_text_not_nfc":LintBool(),
    "w_ext_cert_policy_explicit_text_not_utf8":LintBool(),
    "w_ext_crl_distribution_marked_critical":LintBool(),
    "w_ext_ian_critical":LintBool(),
    "w_ext_key_usage_not_critical":LintBool(),
    "w_ext_policy_map_not_critical":LintBool(),
    "w_ext_policy_map_not_in_cert_policy":LintBool(),
    "w_ext_san_critical_with_subject_dn":LintBool(),
    "w_ext_subject_key_identifier_missing_sub_cert":LintBool(),
    "w_ian_iana_pub_suffix_empty":LintBool(),
    "w_issuer_dn_leading_whitespace":LintBool(),
    "w_issuer_dn_trailing_whitespace":LintBool(),
    "w_multiple_issuer_rdn":LintBool(),
    "w_multiple_subject_rdn":LintBool(),
    "w_name_constraint_on_edi_party_name":LintBool(),
    "w_name_constraint_on_registered_id":LintBool(),
    "w_name_constraint_on_x400":LintBool(),
    "w_root_ca_basic_constraints_path_len_constraint_field_present":LintBool(),
    "w_root_ca_contains_cert_policy":LintBool(),
    "w_rsa_mod_factors_smaller_than_752":LintBool(),
    "w_rsa_mod_not_odd":LintBool(),
    "w_rsa_public_exponent_not_in_range":LintBool(),
    "w_san_iana_pub_suffix_empty":LintBool(),
    "w_serial_number_low_entropy":LintBool(),
    "w_sub_ca_aia_does_not_contain_issuing_ca_url":LintBool(),
    "w_sub_ca_certificate_policies_marked_critical":LintBool(),
    "w_sub_ca_eku_critical":LintBool(),
    "w_sub_ca_name_constraints_not_critical":LintBool(),
    "w_sub_cert_aia_does_not_contain_issuing_ca_url":LintBool(),
    "w_sub_cert_certificate_policies_marked_critical":LintBool(),
    "w_sub_cert_eku_extra_values":LintBool(),
    "w_sub_cert_sha1_expiration_too_long":LintBool(),
    "w_subject_dn_leading_whitespace":LintBool(),
    "w_subject_dn_trailing_whitespace":LintBool(),
})


ZLint = SubRecord({
    "version":Unsigned16BitInteger(),
    "notices_present":Boolean(),
    "warnings_present":Boolean(),
    "errors_present":Boolean(),
    "fatals_present":Boolean(),
    "lints":Lints,
})

certificate = Record({
    "parsed": zcrypto.ParsedCertificate(),
    "raw":Binary(),
    "fingerprint_sha256":HexString(),
    "tags":ListOf(CensysString()),
    "metadata":SubRecord({
        "updated_at":Timestamp(),
        "added_at":Timestamp(),
        "post_processed":Boolean(),
        "post_processed_at":Timestamp(),
        "seen_in_scan":Boolean(),
        "source":String(),
        "parse_version":Unsigned16BitInteger(),
        "parse_error":CensysString(),
        "parse_status":String(),
    }, category="Metadata"),
    "parents":ListOf(String(), category="Misc"),
    "parent_spki_subject_fingerprint":HexString(),
    "validation":SubRecord({
        "nss":ztag_certificate_validation.new(category="NSS (Firefox) Validation"),
        "apple":ztag_certificate_validation.new(category="Apple Validation"),
        "microsoft":ztag_certificate_validation.new(category="Microsoft Validation"),
        #"java":ztag_certificate_validation,
        #"android":ztag_certificate_validation,
        "google_ct_primary":ztag_certificate_validation.new(category="Google CT Validation"),
        #"google_ct_submariner":ztag_certificate_validation,
    }),
    "ct":CTStatus.new(category="Certificate Transparency Logs"),
    "audit":CertificateAudit,
    "zlint":ZLint.new(category="ZLint"),
    "precert":Boolean(category="Misc")
})

zschema.registry.register_schema("certificate", certificate)

#
# The protocol_* types are the primary encodings emitted by
# Grab. Think of them as the entirety of what we collect when we
# discover that a particular service exists, anywhere.
#

protocol_http_type = SubRecordType({
    "get": probe_http_request_type(),
}, type_name="protocol_http")

protocol_https_type = SubRecordType({
    "tls": probe_tls_type(),
    "heartbleed": probe_tls_heartbleed_type(),
    "dhe": probe_tls_dh_type(),
    "rsa_export": probe_tls_rsa_export_type(),
    "dhe_export": probe_tls_dh_export_type(),
    #"ssl_2": probe_tls_sslv2_type(), # XXX
    "ssl_3": probe_tls_support_type(),
    "tls_1_1": probe_tls_support_type(),
    "tls_1_2": probe_tls_support_type(),
    #"tls_1_3": probe_tls_support_type(),
    "ecdhe": probe_tls_ecdh_type(),
    #"extended_random": probe_tls_extended_random_type(),
}, type_name="protocol_https")

protocol_smtp_type = SubRecordType({
    "starttls": probe_smtp_starttls_banner_type(),
    #"ssl_2": probe_tls_sslv2_type(), # XXX
}, type_name = "protocol_smtp")

protocol_telnet_type = SubRecordType({
    "banner": probe_telnet_banner_type(),
}, type_name = "protocol_telnet")

protocol_ftp_type = SubRecordType({
    "banner": probe_ftp_banner_type(),
}, type_name = "protocol_ftp")

protocol_s7_type = SubRecordType({
    "szl": probe_s7_szl_type(),
}, type_name = "protocol_s7")

protocol_pop3_type = SubRecordType({
    "starttls": probe_mail_starttls_banner_type(),
    #"ssl_2": probe_sslv2, # XXX
}, type_name = "protocol_pop3")

protocol_imap_type = SubRecordType({
    "starttls": probe_mail_starttls_banner_type(),
    #"ssl_2": probe_sslv2, # XXX
}, type_name = "protocol_imap") 

protocol_smb_type = SubRecordType({
    "banner": probe_smb_banner_type(),
}, type_name = "protocol_smb")

protocol_modbus_type = SubRecordType({
    "device_id": probe_modbus_device_id_type()
}, type_name = "protocol_modbus")

protocol_ssh_type = SubRecordType({
    "v2": probe_ssh_v2_type(),
}, type_name = "protocol_ssh")

protocol_dns_type = SubRecordType({
    "lookup": probe_dns_lookup_type(),
}, type_name = "protocol_dns")

protocol_bacnet_type = SubRecordType({
    "device_id": probe_bacnet_device_id_type(),
}, type_name = "protocol_bacnet")

protocol_fox_type = SubRecordType({
    "device_id":probe_fox_device_id_type(),
}, type_name = "protocol_fox")

protocol_dnp3_type = SubRecordType({
    "status":probe_dnp3_status_type(),
}, type_name = "protocol_dnp3")

protocol_cwmp_type = SubRecordType({
    "get": probe_http_request_type(),
}, type_name = "protocol_cwmp")

protocol_upnp_type = SubRecordType({
    "discovery": probe_upnp_discovery_type(),
}, type_name = "protocol_upnp") 

protocol_oracle_type = SubRecordType({
    "banner": ztag_oracle,
}, type_name = "protocol_oracle")

protocol_mssql_type = SubRecordType({
    "banner": ztag_mssql,
}, type_name = "protocol_mssql")

protocol_mysql_type = SubRecordType({
    "banner": ztag_mysql,
}, type_name = "protocol_mysql")

protocol_postgres_type = SubRecordType({
    "banner": ztag_postgres,
}, type_name = "protocol_postgres")

ipv4_host = Record({
            Port(443):SubRecord({
                "https": protocol_https_type(category="443/HTTPS"),
            }),
            Port(80):SubRecord({
                "http": protocol_http_type(category="80/HTTP"),
            }),
            Port(8080):SubRecord({
                "http": protocol_http_type(category="8080/HTTP"),
            }),
            Port(8888):SubRecord({
                "http": protocol_http_type(category="8888/HTTP"),
            }),
            Port(25):SubRecord({
                "smtp": protocol_smtp_type(category="25/SMTP"),
            }),
            Port(23):SubRecord({
                "telnet": protocol_telnet_type(category="23/Telnet"),
            }),
            Port(2323):SubRecord({
                "telnet": protocol_telnet_type(category="2323/Telnet"),
            }),
            Port(21):SubRecord({
                "ftp": protocol_ftp_type(category="21/FTP"),
            }),
            Port(102):SubRecord({
                "s7": protocol_s7_type(category="102/S7"),
            }),
            Port(110):SubRecord({
                "pop3": protocol_pop3_type(category="110/POP3"),
            }),
            Port(143): SubRecord({
                "imap": protocol_imap_type(category="143/IMAP"),
            }),
            Port(445):SubRecord({
                "smb": protocol_smb_type(category="445/SMB", validation_policy="error"),
            }),
            Port(993):SubRecord({
                "imaps": protocol_imap_type(category="993/IMAPS"),
            }),
            Port(995):SubRecord({
                "pop3s": protocol_pop3_type(category="995/POP3S"),
            }),
            Port(587):SubRecord({
                "smtp": protocol_smtp_type(category="587/SMTP"),
            }),
            Port(502):SubRecord({
                "modbus": protocol_modbus_type(category="502/Modbus"),
            }),
            Port(22):SubRecord({
                "ssh": protocol_ssh_type(category="22/SSH"),
            }),
            Port(53):SubRecord({
                "dns": protocol_dns_type(category="53/DNS"),
            }),
            Port(47808):SubRecord({
                "bacnet": protocol_bacnet_type(category="47808/BACNET"),
            }),
            Port(1911):SubRecord({
                "fox": protocol_fox_type(category="1911/Fox"),
            }),
            Port(20000):SubRecord({
                "dnp3": protocol_dnp3_type(category="20000/DNP3"),
            }),
            Port(7547):SubRecord({
                "cwmp": protocol_cwmp_type(category="7547/CWMP"),
            }),
            Port(1900):SubRecord({
                "upnp": protocol_upnp_type(category="1900/UPnP"),
            }),
            Port(1521):SubRecord({
                "oracle": protocol_oracle_type(category="1521/Oracle"),
            }),
            Port(1433):SubRecord({
                "mssql": protocol_mssql_type(category="1433/MSSQL"),
            }),
            Port(3306): SubRecord({
                "mysql": protocol_mysql_type(category="3306/MySQL"),
            }),
            Port(5432): SubRecord({
                "postgres": protocol_postgres_type(category="5432/Postgres"),
            }),
            "tags":ListOf(CensysString(), category="Basic Information"),
            "metadata":zdb_metadata,
            "location":zdb_location,
            "__restricted_location":zdb_restricted_location,
            "autonomous_system":zdb_as.new(category="Basic Information"),
            "notes":CensysString(),
            "ip":IPv4Address(required=True, category="Basic Information"),
            "ipint":Unsigned32BitInteger(required=True, doc="Integer value of IP address in host order"),
            "updated_at":Timestamp(),
            "zdb_version":Unsigned32BitInteger(),
            "protocols":ListOf(CensysString(exclude=["bigquery"]), category="Basic Information"),
            "ports":ListOf(Unsigned16BitInteger())
})

website = Record({
            Port(443):SubRecord({
                "https": protocol_https_type(),
                "https_www": SubRecord({
                    "tls": probe_tls_type(),
                })
            }, category="443/HTTPS"),
            Port(80):SubRecord({
                "http": protocol_http_type(),
                "http_www": protocol_http_type(),
            }, category="80/HTTP"),
            Port(25):SubRecord({
                "smtp": protocol_smtp_type(),
            }, category="25/SMTP"),
            Port(0):SubRecord({
                "lookup":SubRecord({
                    "spf":ztag_lookup_spf,
                    "dmarc":ztag_lookup_dmarc,
                    "axfr":ztag_lookup_axfr,
                }),
            }, category="Basic Information"),

            "tags":ListOf(CensysString(), category="Basic Information"),
            "metadata":zdb_metadata,
            "notes":EnglishString(es_include_raw=True),
            "domain":String(category="Basic Information"),
            "alexa_rank":Unsigned32BitInteger(doc="Rank in the Alexa Top 1 Million. "
                    "Null if not currently in the Top 1 Million sites.",
                    category="Basic Information"),
            "updated_at":Timestamp(),
            "zdb_version":Unsigned32BitInteger(),
            "protocols":ListOf(String(), category="Basic Information"),
            "ports":ListOf(Unsigned16BitInteger())
})

DROP_KEYS = {'ip_address', 'metadata', 'tags', 'timestamp'}

zschema.registry.register_schema("ipv4host", ipv4_host)
zschema.registry.register_schema("website", website)
