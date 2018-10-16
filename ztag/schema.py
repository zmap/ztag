from zschema.leaves import *
from zschema.compounds import *

import zschema.registry

from ztag.annotation import Annotation

import zcrypto_schemas.zcrypto as zcrypto
import zgrab2_schemas.zgrab2 as zgrab2
import zgrab2_schemas.zgrab2.mssql as zgrab2_mssql
import zgrab2_schemas.zgrab2.oracle as zgrab2_oracle
import zgrab2_schemas.zgrab2.ssh as zgrab2_ssh

__local_metadata = {}
for key in Annotation.LOCAL_METADATA_KEYS:
    __local_metadata[key] = WhitespaceAnalyzedString()
local_metadata = SubRecord(__local_metadata)

ztag_dh_export = SubRecord({
    "dh_params": zcrypto.DHParams(doc="The parameters for the key."),
    "support": Boolean(),
    "metadata": local_metadata,
    "timestamp": Timestamp(),
})

ztag_dh = SubRecord({
    "dh_params": zcrypto.DHParams(doc="The parameters for the key."),
    "support": Boolean(),
    "metadata": local_metadata,
    "timestamp": Timestamp(),
})

ztag_rsa_export = SubRecord({
    "rsa_params":zcrypto.RSAPublicKey(),
    "support":Boolean(),
    "metadata":local_metadata,
    "timestamp":Timestamp(),
})

ztag_ecdh = SubRecord({
    "ecdh_params":zcrypto.ECDHParams(),
    "support":Boolean(),
    "metadata":local_metadata,
    "timestamp":Timestamp(),
})

zgrab_certificate_trust = SubRecord({
    "type":Enum(doc="root, intermediate, or leaf certificate"),
    "trusted_path":Boolean(doc="Does certificate chain up to browser root store"),
    "valid":Boolean(doc="is this certificate currently valid in this browser"),
    "was_valid":Boolean(doc="was this certificate ever valid in this browser")
})

_zcrypto_parsed_cert = zcrypto.ParsedCertificate()

zgrab_certificate = SubRecord({
    "parsed": SubRecord({
        "__expanded_names": ListOf(String()),
    }, extends=_zcrypto_parsed_cert),
    "validation":SubRecord({
        "nss":zgrab_certificate_trust.new(category="NSS (Firefox) Validation"),
        "apple":zgrab_certificate_trust.new(category="Apple Validation"),
        "microsoft":zgrab_certificate_trust.new(category="Microsoft Validation"),
        "android":zgrab_certificate_trust,
        "java":zgrab_certificate_trust,
    }),
})


zgrab_server_certificate_valid = SubRecord({
    "complete_chain":Boolean(doc="does server provide a chain up to a root"),
    "valid":Boolean(doc="is this certificate currently valid in this browser"),
    "error":WhitespaceAnalyzedString()
})

ztag_tls_type = SubRecordType({
    # This is server_hello.version.name
    "version": zcrypto.TLSVersionName(),
    # cipher_suite = { id: server_hello.cipher_suite.hex, name: server_hello.cipher_suite.name }
    "cipher_suite": SubRecord({
        "id": String(doc="The hexadecimal string representation of the numeric cipher algorithm identifier."),
        "name": WhitespaceAnalyzedString(
            doc="The algorithm identifier for the cipher algorithm identifier, see e.g. https://www.iana.org/assignments/tls-parameters/tls-parameters.xhtml.",
            examples=["unknown", "TLS_RSA_WITH_RC4_128_MD5", "TLS_KRB5_WITH_3DES_EDE_CBC_SHA", "TLS_ECDHE_PSK_WITH_AES_128_GCM_SHA256"],
        ),
    }),
    # server_hello.ocsp_stapling
    "ocsp_stapling": Boolean(),
    # server_hello.secure_renegotiation
    "secure_renegotiation": Boolean(),
    # certificate.parsed = server_certificates.certificate.parsed
    "certificate": zgrab_certificate,
    # chain.parsed = [ elt.parsed for elt in server_certificates.chain ]
    "chain": ListOf(zgrab_certificate),
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
        "signature_error": WhitespaceAnalyzedString(),
        # ... = signature.signature_and_hash_type.signature_algorithm
        "signature_algorithm": String(),
        # ... = signature.signature_and_hash_type.hash_algorithm
        "hash_algorithm": String(),
    }),
    "metadata": local_metadata,
    "timestamp": Timestamp(),
})

ztag_tls = ztag_tls_type()

ztag_heartbleed = SubRecord({
    "heartbeat_enabled":Boolean(),
    "heartbleed_vulnerable":Boolean(),
    "metadata":local_metadata,
    "timestamp":Timestamp(),
})

ztag_smtp_starttls = SubRecord({
    "banner": WhitespaceAnalyzedString(),
    "ehlo": WhitespaceAnalyzedString(),
    "starttls": WhitespaceAnalyzedString(),
    "tls": ztag_tls,
    "metadata":local_metadata,
    "timestamp":Timestamp(),
})

ztag_mail_starttls = SubRecord({
    "banner": WhitespaceAnalyzedString(),
    "starttls": WhitespaceAnalyzedString(),
    "tls": ztag_tls,
    "metadata": local_metadata,
    "timestamp":Timestamp(),
})

ztag_mail_tls = SubRecord({
    "tls":ztag_tls,
    "banner": WhitespaceAnalyzedString(),
    "metadata":local_metadata,
    "timestamp":Timestamp(),
})

zgrab_unknown_http_header = SubRecord({
    "key":String(),
    "value":WhitespaceAnalyzedString()
})

zgrab_http_headers = SubRecord({
    "access_control_allow_origin":WhitespaceAnalyzedString(),
    "accept_patch":WhitespaceAnalyzedString(),
    "accept_ranges":WhitespaceAnalyzedString(),
    "age":WhitespaceAnalyzedString(),
    "allow":WhitespaceAnalyzedString(),
    "alt_svc":WhitespaceAnalyzedString(),
    "alternate_protocol":WhitespaceAnalyzedString(),
    "cache_control":WhitespaceAnalyzedString(),
    "connection":WhitespaceAnalyzedString(),
    "content_disposition":WhitespaceAnalyzedString(),
    "content_encoding":WhitespaceAnalyzedString(),
    "content_language":WhitespaceAnalyzedString(),
    "content_length":WhitespaceAnalyzedString(),
    "content_location":WhitespaceAnalyzedString(),
    "content_md5":WhitespaceAnalyzedString(),
    "content_range":WhitespaceAnalyzedString(),
    "content_type":WhitespaceAnalyzedString(),
    "date":WhitespaceAnalyzedString(),
    "etag":WhitespaceAnalyzedString(),
    "expires":WhitespaceAnalyzedString(),
    "last_modified":WhitespaceAnalyzedString(),
    "link":WhitespaceAnalyzedString(),
    "location":WhitespaceAnalyzedString(),
    "p3p":WhitespaceAnalyzedString(),
    "pragma":WhitespaceAnalyzedString(),
    "proxy_authenticate":WhitespaceAnalyzedString(),
    "public_key_pins":WhitespaceAnalyzedString(),
    "refresh":WhitespaceAnalyzedString(),
    "referer":WhitespaceAnalyzedString(),
    "retry_after":WhitespaceAnalyzedString(),
    "server":WhitespaceAnalyzedString(),
    "set_cookie":WhitespaceAnalyzedString(),
    "status":WhitespaceAnalyzedString(),
    "strict_transport_security":WhitespaceAnalyzedString(),
    "trailer":WhitespaceAnalyzedString(),
    "transfer_encoding":WhitespaceAnalyzedString(),
    "upgrade":WhitespaceAnalyzedString(),
    "vary":WhitespaceAnalyzedString(),
    "via":WhitespaceAnalyzedString(),
    "warning":WhitespaceAnalyzedString(),
    "www_authenticate":WhitespaceAnalyzedString(),
    "x_frame_options":WhitespaceAnalyzedString(),
    "x_xss_protection":WhitespaceAnalyzedString(),
    "content_security_policy":WhitespaceAnalyzedString(),
    "x_content_security_policy":WhitespaceAnalyzedString(),
    "x_webkit_csp":WhitespaceAnalyzedString(),
    "x_content_type_options":WhitespaceAnalyzedString(),
    "x_powered_by":WhitespaceAnalyzedString(),
    "x_ua_compatible":WhitespaceAnalyzedString(),
    "x_content_duration":WhitespaceAnalyzedString(),
    "x_forwarded_for":WhitespaceAnalyzedString(),
    "x_real_ip":WhitespaceAnalyzedString(),
    "proxy_agent":WhitespaceAnalyzedString(),
    "unknown":ListOf(zgrab_unknown_http_header)
})

ztag_http = SubRecord({
    "status_code":Unsigned16BitInteger(),
    "status_line":WhitespaceAnalyzedString(),
    "body":HTML(),
    "headers":zgrab_http_headers,
    "body_sha256":HexString(validation_policy="warn"),
    "title":WhitespaceAnalyzedString(),
    "metadata":local_metadata,
    "timestamp":Timestamp(),
})

golang_crypto_param = SubRecord({
    "value":IndexedBinary(),
    "length":Unsigned32BitInteger()
})

#ztag_open_proxy = SubRecord({
#    "connect":SubRecord({
#      "status_code":Integer(),
#      "status_line":WhitespaceAnalyzedString(),
#      "body":WhitespaceAnalyzedString(),
#      "headers":zgrab_http_headers
#    }),
#    "get":SubRecord({
#      "status_code":Integer(),
#      "status_line":WhitespaceAnalyzedString(),
#      "body":WhitespaceAnalyzedString(),
#      "headers":zgrab_http_headers,
#      "random_present":Boolean(),
#      "body_sha256":HexString()
#    }),
#    "metadata":local_metadata
#})

# 2018/09/07: Workaround for mis-typed CertType.id field in ES; actual type is uint32, current ES
# type is keyword (string).
ssh_certkey_public_key_type = zgrab2_ssh.CertType(exclude={"bigquery"})
ssh_certkey_public_key_type["id"].set("exclude",
                                      ssh_certkey_public_key_type["id"].exclude |
                                      {"elasticsearch"})

ztag_ssh_v2 = SubRecord({
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
            "type": ssh_certkey_public_key_type,
            "key_id": String(),
            "valid_principals": ListOf(String()),
            "validity": SubRecord({
                # These are DateTimes in SSHPublicKeyCert
                "valid_after": Timestamp(doc="Timestamp of when certificate is first valid. Timezone is UTC."),
                "valid_before": Timestamp(doc="Timestamp of when certificate expires. Timezone is UTC."),
                "length": Signed64BitInteger(),
            }),
            "reserved": Binary(),
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
                "value": Binary(),
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
})

ztag_ftp = SubRecord({
    "banner":WhitespaceAnalyzedString(),
    "metadata":local_metadata,
    "timestamp":Timestamp(),
})

telnet_caps_list = ListOf(SubRecord({
    "name":String(),
    "value":Unsigned32BitInteger()
}))

ztag_telnet = SubRecord({
    "support":Boolean(),
    "banner":WhitespaceAnalyzedString(),
    "will":telnet_caps_list,
    "wont":telnet_caps_list,
    "do":telnet_caps_list,
    "dont":telnet_caps_list,
    "metadata":local_metadata,
    "timestamp":Timestamp(),
})

ztag_modbus = SubRecord({
    "support":Boolean(),
    "function_code":Unsigned16BitInteger(),
    "mei_response":SubRecord({
      "conformity_level":Signed32BitInteger(),
      "objects":SubRecord({
        "vendor":WhitespaceAnalyzedString(),
        "product_code":WhitespaceAnalyzedString(),
        "revision":WhitespaceAnalyzedString(),
        "vendor_url":URL(),
        "product_name":WhitespaceAnalyzedString(),
        "model_name":WhitespaceAnalyzedString(),
        "user_application_name":WhitespaceAnalyzedString(),
      })
    }),
    "metadata":local_metadata,
    "timestamp":Timestamp(),
})

ztag_bacnet = SubRecord({
    "support":Boolean(),
    "instance_number": Signed32BitInteger(),
    "vendor": SubRecord({
        "id": Signed32BitInteger(),
        "reported_name":WhitespaceAnalyzedString(),
        "official_name":WhitespaceAnalyzedString(),
    }),
    "firmware_revision": String(),
    "application_software_revision":String(),
    "object_name":WhitespaceAnalyzedString(),
    "model_name":WhitespaceAnalyzedString(),
    "description":WhitespaceAnalyzedString(),
    "location":WhitespaceAnalyzedString(),
    "metadata":local_metadata,
    "timestamp":Timestamp(),
})

ztag_dns_question = SubRecord({
    "name":String(),
    "type":String()
})


ztag_dns_answer = SubRecord({
    "name":String(),
    "response":WhitespaceAnalyzedString(),
    "type":String()
})

ztag_dns_lookup = SubRecord({
    "support":Boolean(),
    "errors":Boolean(),
    "open_resolver":Boolean(),
    "resolves_correctly":Boolean(),
    "answers":ListOf(ztag_dns_answer),
    "authorities":ListOf(ztag_dns_answer),
    "additionals":ListOf(ztag_dns_answer),
    "questions":ListOf(ztag_dns_question),
    "metadata":local_metadata,
    "timestamp":Timestamp(),
})

ztag_tls_support = SubRecord({
    "support": Boolean(),
    "metadata":local_metadata,
    "timestamp":Timestamp(),
})

ztag_fox = SubRecord({
    "support":Boolean(),
    "version":WhitespaceAnalyzedString(),
    "id":Signed32BitInteger(),
    "hostname":WhitespaceAnalyzedString(),
    "host_address":WhitespaceAnalyzedString(),
    "app_name":WhitespaceAnalyzedString(),
    "app_version":WhitespaceAnalyzedString(),
    "vm_name":WhitespaceAnalyzedString(),
    "vm_version":WhitespaceAnalyzedString(),
    "os_name":WhitespaceAnalyzedString(),
    "os_version":WhitespaceAnalyzedString(),
    "station_name":WhitespaceAnalyzedString(),
    "language":WhitespaceAnalyzedString(),
    "time_zone":WhitespaceAnalyzedString(),
    "host_id":WhitespaceAnalyzedString(),
    "vm_uuid":WhitespaceAnalyzedString(),
    "brand_id":WhitespaceAnalyzedString(),
    "sys_info":WhitespaceAnalyzedString(),
    "auth_agent_type":String(),
    "metadata":local_metadata,
    "timestamp":Timestamp(),
})

ztag_dnp3 = SubRecord({
    "support":Boolean(),
    "raw_response":Binary(),
    "metadata":local_metadata,
    "timestamp":Timestamp(),
})

ztag_s7 = SubRecord({
    "support":Boolean(),
    "system":WhitespaceAnalyzedString(),
    "module":WhitespaceAnalyzedString(),
    "plant_id":WhitespaceAnalyzedString(),
    "copyright":WhitespaceAnalyzedString(),
    "serial_number":WhitespaceAnalyzedString(),
    "reserved_for_os":WhitespaceAnalyzedString(),
    "module_type":WhitespaceAnalyzedString(),
    "memory_serial_number":WhitespaceAnalyzedString(),
    "cpu_profile":WhitespaceAnalyzedString(),
    "oem_id":WhitespaceAnalyzedString(),
    "location":WhitespaceAnalyzedString(),
    "module_id":WhitespaceAnalyzedString(),
    "hardware":WhitespaceAnalyzedString(),
    "firmware":WhitespaceAnalyzedString(),
    "metadata":local_metadata,
    "timestamp":Timestamp(),
})

ztag_smb = SubRecord({
    "smbv1_support":Boolean(),
    "metadata":local_metadata,
})

ztag_upnp_discovery = SubRecord({
    "usn": WhitespaceAnalyzedString(),
    "agent": WhitespaceAnalyzedString(),
    "st": WhitespaceAnalyzedString(),
    "ext": WhitespaceAnalyzedString(),
    "location": WhitespaceAnalyzedString(),
    "server": WhitespaceAnalyzedString(),
    "cache_control": WhitespaceAnalyzedString(),
    "x_user_agent": WhitespaceAnalyzedString(),
    "metadata": local_metadata,
})

# Add the common zgrab2 fields to the results schema which are added by
# ZGrab2Transform._transform_object().
def ztag_zgrab2_transformed(service, results):
    results["supported"] = Boolean(doc="If true, %s was detected on this machine." % service)
    results["metadata"] = local_metadata
    return results

# The oracle ztag transform is a plain copy of the "handshake" field.
ztag_oracle = ztag_zgrab2_transformed(service="Oracle", results=zgrab2_oracle.oracle_scan_response["result"]["handshake"])

ztag_oracle["tls"] = ztag_tls_type(doc="The TLS handshake with the server (if applicable).")

ztag_mssql = ztag_zgrab2_transformed(service="MSSQL", results=SubRecord({
    "version": WhitespaceAnalyzedString(doc="The MSSQL version returned by the server in "
                                "the PRELOGIN response. Its format is "
                                "'MAJOR.MINOR.BUILD_NUMBER'."),
    "instance_name": WhitespaceAnalyzedString(doc="The value of the INSTANCE field "
                                      "returned by the server in the PRELOGIN "
                                      "response."),
    "encrypt_mode": Enum(values=zgrab2_mssql.ENCRYPT_MODES,
                         doc="The negotiated encryption mode for the session. "
                             "See https://msdn.microsoft.com/en-us/library/dd357559.aspx "
                             "for details."),
    "tls": ztag_tls_type(doc="The TLS handshake with the server (for "
                             "non-encrypted connections, this used only "
                             "for the authentication phase).")
}))

ztag_mysql = ztag_zgrab2_transformed(service="MySQL", results=SubRecord({
    "protocol_version": zgrab2.mysql.mysql_scan_response["result"]["protocol_version"],
    "server_version": zgrab2.mysql.mysql_scan_response["result"]["server_version"],
    "capability_flags": zgrab2.mysql.mysql_capability_flags,
    "status_flags": zgrab2.mysql.mysql_server_status_flags,
    "error_code": zgrab2.mysql.mysql_scan_response["result"]["error_code"],
    "error_id": zgrab2.mysql.mysql_scan_response["result"]["error_id"],
    "error_message": zgrab2.mysql.mysql_scan_response["result"]["error_message"],
    "tls": ztag_tls_type(doc="If the server allows upgrading the "
                             "session to use TLS, this is the log of "
                             "the handshake.")
}))

ztag_mongodb = ztag_zgrab2_transformed(service="MongoDB", results=SubRecord({
        "build_info": SubRecord({
            "version": WhitespaceAnalyzedString(doc="Version of mongodb server"),
            "git_version": WhitespaceAnalyzedString(doc="Git Version of mongodb server"),
            "max_wire_version": Signed32BitInteger(),
            "build_environment": SubRecord({
                "dist_mod": WhitespaceAnalyzedString(),
                "dist_arch": WhitespaceAnalyzedString(),
                "cc": WhitespaceAnalyzedString(),
                "cc_flags": WhitespaceAnalyzedString(),
                "cxx": WhitespaceAnalyzedString(),
                "cxx_flags": WhitespaceAnalyzedString(),
                "link_flags": WhitespaceAnalyzedString(),
                "target_arch": WhitespaceAnalyzedString(),
                "target_os": WhitespaceAnalyzedString()
            })
        }, doc="Result of issuing the buildInfo command see https://docs.mongodb.com/manual/reference/command/buildInfo"),
        "is_master": SubRecord({
            "is_master": Boolean(),
            "max_wire_version": Signed32BitInteger(),
            "min_wire_version": Signed32BitInteger(),
            "max_bson_object_size": Signed32BitInteger(),
            "max_write_batch_size": Signed32BitInteger(),
            "logical_session_timeout_minutes": Signed32BitInteger(),
            "max_message_size_bytes": Signed32BitInteger(),
            "read_only": Boolean()
        }, doc="Result of issuing the isMaster command see https://docs.mongodb.com/manual/reference/command/isMaster")
}))

ztag_postgres = ztag_zgrab2_transformed(service="PostgreSQL", results=SubRecord({
    "supported_versions": WhitespaceAnalyzedString(doc="The error string returned by the "
                                           "server in response to a "
                                           "StartupMessage with "
                                           "ProtocolVersion = 0.0"),
    "protocol_error": zgrab2.postgres.postgres_error,
    "startup_error": zgrab2.postgres.postgres_error,
    "is_ssl": Boolean(doc="If the server supports TLS and the session was "
                          "updated to use TLS, this is true."),
    "authentication_mode": zgrab2.postgres.postgres_auth_mode["mode"],
    "backend_key_data": zgrab2.postgres.postgres_key_data,
    "tls": ztag_tls_type(doc="If the server allows upgrading the "
                             "session to use TLS, this is the log of "
                             "the handshake.")
}))

ztag_ipp = ztag_zgrab2_transformed(service="IPP", results=SubRecord({
    "version_major": zgrab2.ipp.ipp_scan_response["result"]["version_major"],
    "version_minor": zgrab2.ipp.ipp_scan_response["result"]["version_minor"],
    "version_string": zgrab2.ipp.ipp_scan_response["result"]["version_string"],
    "cups_version": zgrab2.ipp.ipp_scan_response["result"]["cups_version"],
    "attributes": zgrab2.ipp.ipp_scan_response["result"]["attributes"],
    "attr_ipp_versions": zgrab2.ipp.ipp_scan_response["result"]["attr_ipp_versions"],
    "attr_cups_version": zgrab2.ipp.ipp_scan_response["result"]["attr_cups_version"],
    "attr_printer_uris": zgrab2.ipp.ipp_scan_response["result"]["attr_printer_uris"],
    "tls": ztag_tls_type(doc="If the server allows upgrading the "
                             "session to use TLS, this is the log of "
                             "the handshake."),
}))

ztag_schemas = [
    ("ztag_https", ztag_tls),
    ("ztag_heartbleed", ztag_heartbleed),
    ("ztag_smtp_starttls", ztag_smtp_starttls),
    ("ztag_imap_starttls", ztag_mail_starttls),
    ("ztag_pop3_starttls", ztag_mail_starttls),
    ("ztag_imap_tls", ztag_mail_tls),
    ("ztag_pop3_tls", ztag_mail_tls),
    ("ztag_http", ztag_http),
    ("ztag_ftp", ztag_ftp),
    ("ztag_dh", ztag_dh),
    ("ztag_dh_export", ztag_dh_export),
    ("ztag_rsa_export", ztag_rsa_export),
    ("ztag_ecdh", ztag_ecdh),
    ("ztag_sslv3", ztag_tls_support),
    ("ztag_tls1", ztag_tls_support),
    ("ztag_tls2", ztag_tls_support),
    ("ztag_tls3", ztag_tls_support),
    ("ztag_modbus", ztag_modbus),
    ("ztag_ssh_v2", ztag_ssh_v2),
    ("ztag_dns_lookup", ztag_dns_lookup),
    ("ztag_bacnet", ztag_bacnet),
    ("ztag_fox", ztag_fox),
    ("ztag_dnp3", ztag_dnp3),
    ("ztag_s7", ztag_s7),
    ("ztag_smb", ztag_smb),
    ("ztag_upnp_discovery", ztag_upnp_discovery),
    ("ztag_oracle", ztag_oracle),
    ("ztag_mssql", ztag_mssql),
    ("ztag_ipp", ztag_ipp),
    ("ztag_mongodb", ztag_mongodb),
]
for (name, schema) in ztag_schemas:
    x = Record({
        "ip_address":IPAddress(required=True),
        #"timestamp":Timestamp(required=True),
        "tags":ListOf(String()),
        "metadata": SubRecord({}, allow_unknown=True),
    }, extends=schema)
    zschema.registry.register_schema("%s" % name, x)


ztag_lookup_spf = SubRecord({
    "raw":WhitespaceAnalyzedString(),
})

ztag_lookup_dmarc = SubRecord({
    "raw":WhitespaceAnalyzedString(),
    "p":String(),
})

ztag_lookup_axfr = SubRecord({
    "servers":ListOf(SubRecord({
        "server":String(),
        "status":String(),
        "name":FQDN(),
        "support":Boolean(),
        "error":WhitespaceAnalyzedString(),
        "records":ListOf(SubRecord({
            "algorithm":Unsigned16BitInteger(),
            "answer":String(),
            "class":String(),
            "data":WhitespaceAnalyzedString(),
            "digest":WhitespaceAnalyzedString(),
            "digest_type":Unsigned16BitInteger(),
            "expire":Unsigned32BitInteger(),
            "flag":Unsigned16BitInteger(),
            "flags":Unsigned16BitInteger(),
            "key_tag":Unsigned16BitInteger(),
            "mbox":FQDN(),
            "min_ttl":Unsigned32BitInteger(),
            "name":FQDN(),
            "ns":FQDN(),
            "preference":Signed16BitInteger(),
            "protocol":Unsigned16BitInteger(),
            "public_key":String(),
            "refresh":Signed32BitInteger(),
            "retry":Signed32BitInteger(),
            "serial":Unsigned32BitInteger(),
            "tag":String(),
            "type":String(),
            "ttl":Unsigned32BitInteger(),
            # FIXME 2018/10/15: Conflict with auto-detected version in Elasticsearch (auto type
            # FIXME 2018/10/15: is text, new type is keyword)
            "value": String(exclude={"elasticsearch"}),
        })),
    })),
    "truncated":Boolean(),
    "support":Boolean()
})

_zdb_location_fields = {
    "continent":String(),
    "country":WhitespaceAnalyzedString(),
    "country_code":String(),
    "city":WhitespaceAnalyzedString(),
    "postal_code":String(),
    "timezone":WhitespaceAnalyzedString(),
    "province":WhitespaceAnalyzedString(),
    "latitude":Double(),
    "longitude":Double(),
    "registered_country":WhitespaceAnalyzedString(),
    "registered_country_code":String(),
}

zdb_location = SubRecord(_zdb_location_fields, category="Location")
zdb_restricted_location = SubRecord(_zdb_location_fields, exclude=["bigquery",])

zdb_as = SubRecord({
    "asn":Unsigned32BitInteger(),
    "description":WhitespaceAnalyzedString(),
    "path":ListOf(Unsigned32BitInteger()),
    "rir":String(),
    "routed_prefix":FQDN(),
    "name":WhitespaceAnalyzedString(),
    "country_code":String(),
    "organization":WhitespaceAnalyzedString(),
})


__metadata = {}
for key in Annotation.GLOBAL_METADATA_KEYS:
    __metadata[key] = WhitespaceAnalyzedString()
zdb_metadata = SubRecord(__metadata)

CTServerStatus = SubRecord({
    "index":Signed64BitInteger(),
    "added_to_ct_at":Timestamp(),
    "ct_to_censys_at":Timestamp(),
    "censys_to_ct_at":Timestamp(),
    "sct":IndexedBinary(),
})


CTStatus = SubRecord({
    "google_aviator":CTServerStatus,
    "google_pilot":CTServerStatus,
    "google_rocketeer":CTServerStatus,
    "google_submariner":CTServerStatus,
    "google_testtube":CTServerStatus,
    "google_icarus":CTServerStatus,
    "google_skydiver":CTServerStatus,
    "google_daedalus":CTServerStatus,
    "digicert_ct1":CTServerStatus,
    "izenpe_com_ct":CTServerStatus,
    "izenpe_eus_ct":CTServerStatus,
    "symantec_ws_ct":CTServerStatus,
    "symantec_ws_vega":CTServerStatus,
    "wosign_ctlog":CTServerStatus,
    "wosign_ct":CTServerStatus,
    "cnnic_ctserver":CTServerStatus,
    "gdca_ct":CTServerStatus,
    "startssl_ct":CTServerStatus,
    "certly_log":CTServerStatus,
    "venafi_api_ctlog":CTServerStatus,
    "symantec_ws_deneb":CTServerStatus,
    "nordu_ct_plausible":CTServerStatus,
    "comodo_dodo":CTServerStatus,
    "comodo_mammoth":CTServerStatus,
    "gdca_ctlog":CTServerStatus,
    "symantec_ws_sirius":CTServerStatus,
    "certificatetransparency_cn_ct":CTServerStatus,
    "venafi_api_ctlog_gen2":CTServerStatus,
    "digicert_ct2":CTServerStatus,
    "comodo_sabre":CTServerStatus,
    "sheca_ct":CTServerStatus,
    "letsencrypt_ct_clicky":CTServerStatus,
    "behind_the_sofa":CTServerStatus,
    "gdca_log":CTServerStatus,
    "gdca_log2":CTServerStatus,
    "wotrus_ctlog":CTServerStatus,
    "wotrus_ctlog3":CTServerStatus,
    "akamai_ct":CTServerStatus,
    "google_argon_2017":CTServerStatus,
    "google_argon_2018":CTServerStatus,
    "google_argon_2019":CTServerStatus,
    "google_argon_2020":CTServerStatus,
    "google_argon_2021":CTServerStatus,
    "google_xenon_2018":CTServerStatus,
    "google_xenon_2019":CTServerStatus,
    "google_xenon_2020":CTServerStatus,
    "google_xenon_2021":CTServerStatus,
    "google_xenon_2022":CTServerStatus,
    "cloudflare_nimbus_2017":CTServerStatus,
    "cloudflare_nimbus_2018":CTServerStatus,
    "cloudflare_nimbus_2019":CTServerStatus,
    "cloudflare_nimbus_2020":CTServerStatus,
    "cloudflare_nimbus_2021":CTServerStatus,
    "digicert_nessie_2018":CTServerStatus,
    "digicert_nessie_2019":CTServerStatus,
    "digicert_nessie_2020":CTServerStatus,
    "digicert_nessie_2021":CTServerStatus,
    "digicert_nessie_2022":CTServerStatus,
    "digicert_yeti_2018":CTServerStatus,
    "digicert_yeti_2019":CTServerStatus,
    "digicert_yeti_2020":CTServerStatus,
    "digicert_yeti_2021":CTServerStatus,
    "digicert_yeti_2022":CTServerStatus,
    "digicert_golem":CTServerStatus,
    "izenpe_com_pilot":CTServerStatus,
    "letsencrypt_ct_birch":CTServerStatus,
    "letsencrypt_ct_faux":CTServerStatus,
    "letsencrypt_ct_oak":CTServerStatus,
    "nordu_ct_flimsy":CTServerStatus,
    "sheca_ctlog":CTServerStatus,
    "wosign_ctlog2":CTServerStatus,
    "wosign_ctlog3":CTServerStatus,
    "ctlogs_alpha":CTServerStatus,
})


CertificateAudit = SubRecord({
    "ccadb":SubRecord({
        "current_in_intermediates":Boolean(),
        "was_in_intermediates":Boolean(),
        "owner_name":WhitespaceAnalyzedString(),
        "parent_name":WhitespaceAnalyzedString(),
        "certificate_name":WhitespaceAnalyzedString(),
        "certificate_policy":WhitespaceAnalyzedString(),
        "certification_practice_statement":WhitespaceAnalyzedString(),
        "cp_same_as_parent":Boolean(),
        "audit_same_as_parent":Boolean(),
        "standard_audit":WhitespaceAnalyzedString(),
        "br_audit":WhitespaceAnalyzedString(),
        "auditor":WhitespaceAnalyzedString(),
        "standard_audit_statement_timestamp":Timestamp(),
        "management_assertions_by":WhitespaceAnalyzedString(),
        "comments":EnglishString(es_include_raw=True),
        "ev_policy_oids":WhitespaceAnalyzedString(),
        "approval_bug":WhitespaceAnalyzedString(),
        "first_nss_release":WhitespaceAnalyzedString(),
        "first_firefox_release":WhitespaceAnalyzedString(),
        "ev_audit":WhitespaceAnalyzedString(),
        "current_in_roots":Boolean(),
        "was_in_roots":Boolean(),
        "test_website_valid":WhitespaceAnalyzedString(),
        "mozilla_applied_constraints":WhitespaceAnalyzedString(),
        "company_website":WhitespaceAnalyzedString(),
        "geographic_focus":WhitespaceAnalyzedString(),
        "standard_audit_type":WhitespaceAnalyzedString(),
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
    "paths":NestedListOf(HexString(), "path", validation_policy="ignore"),
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
    "e_basic_constraints_not_critical":LintBool(),
    "e_ca_common_name_missing":LintBool(),
    "e_ca_country_name_invalid":LintBool(),
    "e_ca_country_name_missing":LintBool(),
    "e_ca_crl_sign_not_set":LintBool(),
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
    "e_ext_policy_constraints_not_critical":LintBool(),
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
}, validation_policy="ignore")


ZLint = SubRecord({
    # version is an int64 in the protobuf
    "version":Unsigned16BitInteger(validation_policy="ignore"),
    "notices_present":Boolean(),
    "warnings_present":Boolean(),
    "errors_present":Boolean(),
    "fatals_present":Boolean(),
    "lints":Lints,
})



certificate = Record({
    "parsed": SubRecord({
        "__expanded_names": ListOf(String()),
    }, extends=zcrypto.ParsedCertificate()),
    "raw":Binary(),
    "fingerprint_sha256":HexString(),
    "tags":ListOf(WhitespaceAnalyzedString()),
    "metadata":SubRecord({
        "updated_at":Timestamp(),
        "added_at":Timestamp(),
        "post_processed":Boolean(),
        "post_processed_at":Timestamp(),
        "seen_in_scan":Boolean(),
        "source":String(),
        "parse_version":Unsigned16BitInteger(),
        "parse_error":WhitespaceAnalyzedString(),
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
    # TODO: 2018/08/14 -- ccadb data is not being loaded, so hold off on creating this schema.
    # "audit":CertificateAudit,
    "zlint":ZLint.new(category="ZLint"),
    "precert":Boolean(category="Misc")
})

zschema.registry.register_schema("certificate", certificate)

ipv4_host = Record({
            Port(443):SubRecord({
                "https":SubRecord({
                    "tls":ztag_tls,
                    "get":ztag_http,
                    "heartbleed":ztag_heartbleed,
                    "dhe": ztag_dh,
                    "rsa_export": ztag_rsa_export,
                    "dhe_export": ztag_dh_export,
                    "ssl_3": ztag_tls_support,
                    "tls_1_1": ztag_tls_support,
                    "tls_1_2": ztag_tls_support,
                    "ecdhe": ztag_ecdh,
                }, category="443/HTTPS")
            }),
            Port(80):SubRecord({
                "http":SubRecord({
                    "get":ztag_http,
                }, category="80/HTTP"),
            }),
            Port(8080):SubRecord({
                "http":SubRecord({
                    "get":ztag_http,
                }, category="8080/HTTP"),
            }),
            Port(8888):SubRecord({
                "http":SubRecord({
                    "get":ztag_http,
                }, category="8888/HTTP"),
            }),
            Port(25):SubRecord({
                "smtp":SubRecord({
                    "starttls": ztag_smtp_starttls,
                }, category="25/SMTP"),
            }),
            Port(23):SubRecord({
                "telnet":SubRecord({
                    "banner":ztag_telnet
                }, category="23/Telnet")
            }),
            Port(2323):SubRecord({
                "telnet":SubRecord({
                    "banner":ztag_telnet
                }, category="2323/Telnet")
            }),
            Port(21):SubRecord({
                "ftp":SubRecord({
                  "banner":ztag_ftp,
                }, category="21/FTP")
            }),
            Port(102):SubRecord({
                "s7":SubRecord({
                    "szl":ztag_s7
                }, category="102/S7")
            }),
            Port(110):SubRecord({
                "pop3":SubRecord({
                    "starttls":ztag_mail_starttls,
                }, category="110/POP3")
            }),
            Port(143):SubRecord({
                "imap":SubRecord({
                    "starttls":ztag_mail_starttls,
                }, category="143/IMAP")
            }),
            Port(445):SubRecord({
                "smb":SubRecord({
                    "banner":ztag_smb
                }, category="445/SMB", validation_policy="error")
            }),
            Port(993):SubRecord({
                "imaps":SubRecord({
                    "tls":ztag_mail_tls,
                }, category="993/IMAPS")
            }),
            Port(995):SubRecord({
                "pop3s":SubRecord({
                    "tls":ztag_mail_tls,
                }, category="995/POP3S")
            }),
            Port(587):SubRecord({
                "smtp":SubRecord({
                    "starttls": ztag_smtp_starttls,
                }, category="587/SMTP")
            }),
            Port(502):SubRecord({
                "modbus":SubRecord({
                    "device_id":ztag_modbus
                }, category="502/Modbus")
            }),
            Port(22):SubRecord({
                "ssh":SubRecord({
                    "v2": ztag_ssh_v2
                }, category="22/SSH"),
            }),
            Port(53):SubRecord({
                "dns":SubRecord({
                    "lookup":ztag_dns_lookup
                }, category="53/DNS")
            }),
            Port(47808):SubRecord({
                "bacnet":SubRecord({
                    "device_id":ztag_bacnet
                }, category="47808/BACNET")
            }),
            Port(1911):SubRecord({
                "fox":SubRecord({
                    "device_id":ztag_fox
                }, category="1911/Fox")
            }),
            Port(20000):SubRecord({
                "dnp3":SubRecord({
                    "status":ztag_dnp3,
                }, category="20000/DNP3")
            }),
            Port(7547):SubRecord({
                "cwmp":SubRecord({
                    "get":ztag_http,
                }, category="7547/CWMP")
            }),
            Port(1900):SubRecord({
                "upnp":SubRecord({
                    "discovery":ztag_upnp_discovery,
                }, category="1900/UPnP")
            }),
            Port(1521):SubRecord({
                "oracle":SubRecord({
                    "banner": ztag_oracle,
                }, category="1521/Oracle"),
            }),
            Port(1433):SubRecord({
                "mssql":SubRecord({
                    "banner": ztag_mssql,
                }, category="1433/MSSQL"),
            }),
            Port(3306): SubRecord({
                "mysql": SubRecord({
                    "banner": ztag_mysql,
                }, category="3306/MySQL"),
            }),
            Port(27017): SubRecord({
                "mongodb": SubRecord({
                    "banner": ztag_mongodb ,
                }, category="27017/MongoDB"),
            }),
            Port(5432): SubRecord({
                "postgres": SubRecord({
                    "banner": ztag_postgres,
                }, category="5432/Postgres"),
            }),
            Port(631): SubRecord({
                "ipp": SubRecord({
                    "banner": ztag_ipp,
                }, category="631/IPP"),
            }),
            "tags":ListOf(WhitespaceAnalyzedString(), category="Basic Information"),
            "metadata":zdb_metadata,
            "location":zdb_location,
            "__restricted_location":zdb_restricted_location,
            "autonomous_system":zdb_as.new(category="Basic Information"),
            "notes":WhitespaceAnalyzedString(),
            "ip":IPv4Address(required=True, category="Basic Information"),
            "ipint":Unsigned32BitInteger(required=True, doc="Integer value of IP address in host order"),
            "updated_at":Timestamp(),
            "zdb_version":Unsigned32BitInteger(),
            "protocols":ListOf(String(), category="Basic Information"),
            "ports":ListOf(Unsigned16BitInteger())
})

website = Record({
            Port(443):SubRecord({
                "https":SubRecord({
                    "get":ztag_http,
                    "tls":ztag_tls,
                    "heartbleed":ztag_heartbleed,
                    "dhe": ztag_dh,
                    "rsa_export": ztag_rsa_export,
                    "dhe_export": ztag_dh_export,
                    "ssl_3": ztag_tls_support,
                    "tls_1_1": ztag_tls_support,
                    "tls_1_2": ztag_tls_support,
                    "ecdhe": ztag_ecdh,
                }),
                "https_www":SubRecord({
                    "tls":ztag_tls,
                    "get":ztag_http,
                })
            }, category="443/HTTPS"),
            Port(80):SubRecord({
                "http":SubRecord({
                    "get":ztag_http,
                }),
                "http_www":SubRecord({
                    "get":ztag_http,
                }),
            }, category="80/HTTP"),
            Port(25):SubRecord({
                "smtp":SubRecord({
                    "starttls": ztag_smtp_starttls,
                })
            }, category="25/SMTP"),
            Port(0):SubRecord({
                "lookup":SubRecord({
                    "spf":ztag_lookup_spf,
                    "dmarc":ztag_lookup_dmarc,
                    "axfr":ztag_lookup_axfr,
                })
            }, category="Basic Information"),

            "tags":ListOf(WhitespaceAnalyzedString(), category="Basic Information"),
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
