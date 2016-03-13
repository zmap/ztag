from zschema.leaves import *
from zschema.compounds import *

import zschema.registry

from ztag.annotation import Annotation

__local_metadata = {}
for key in Annotation.LOCAL_METADATA_KEYS:
    __local_metadata[key] = AnalyzedString(es_include_raw=True)
local_metadata = SubRecord(__local_metadata)

zgrab_subj_issuer = SubRecord({
    "serial_number":ListOf(String()),
    "common_name":ListOf(AnalyzedString(es_include_raw=True)),
    "country":ListOf(AnalyzedString(es_include_raw=True)),
    "locality":ListOf(AnalyzedString(es_include_raw=True)),
    "province":ListOf(AnalyzedString(es_include_raw=True)),
    "street_address":ListOf(AnalyzedString(es_include_raw=True)),
    "organization":ListOf(AnalyzedString(es_include_raw=True)),
    "organizational_unit":ListOf(AnalyzedString(es_include_raw=True)),
    "postal_code":ListOf(String()),
})

unknown_extension = SubRecord({
    "id":String(),
    "critical":Boolean(),
    "value":IndexedBinary(),
})

ztag_dh_params = SubRecord({
    "prime":SubRecord({
        "value":IndexedBinary(),
        "length":Integer(),
    }),
    "generator":SubRecord({
        "value":IndexedBinary(),
        "length":Integer(),
    }),
})

ztag_dh_export = SubRecord({
    "dh_params":ztag_dh_params,
    "support": Boolean(),
    "metadata":local_metadata
})

ztag_dh = SubRecord({
    "dh_params":ztag_dh_params,
    "support": Boolean(),
    "metadata":local_metadata
})
ztag_rsa_params = SubRecord({
   "exponent":Long(),
   "modulus":IndexedBinary(),
   "length":Integer(),
})

ztag_rsa_export = SubRecord({
    "rsa_params":ztag_rsa_params,
    "support": Boolean(),
    "metadata":local_metadata
})

ztag_ecdh_params = SubRecord({
    "curve_id":SubRecord({
        "name":String(),
        "id":Integer(),
    })
})

ztag_ecdh = SubRecord({
    "ecdh_params":ztag_ecdh_params,
    "support": Boolean(),
    "metadata":local_metadata
})

zgrab_parsed_certificate = SubRecord({
    "subject":zgrab_subj_issuer,
    "subject_dn":AnalyzedString(es_include_raw=True),
    "issuer":zgrab_subj_issuer,
    "issuer_dn":AnalyzedString(es_include_raw=True),
    "version":Integer(),
    "serial_number":String(doc="Serial number as an unsigned decimal integer. "\
                               "Stored as string to support >uint lengths. "\
                               "Negative values are allowed."),
    "validity":SubRecord({
        "start":DateTime(doc="Timestamp of when certificate is first valid. Timezone is UTC."),
        "end":DateTime(doc="Timestamp of when certificate expires. Timezone is UTC.")
    }),
    "signature_algorithm":SubRecord({
        "name":String(),
        "oid":String(),
    }),
    "subject_key_info":SubRecord({
        "key_algorithm":SubRecord({
            "name":String(doc="Name of public key type, e.g., RSA or ECDSA. "\
                              "More information is available the named SubRecord"\
                              " (e.g., rsa_public_key)."),
            "oid":String(doc="OID of the public key on the certificate. "\
                             "This is helpful when an unknown type is present. "\
                             "This field is reserved and not current populated.")
         }),
        "rsa_public_key":SubRecord({
            "exponent":Long(),
            "modulus":IndexedBinary(),
            "length":Integer(doc="Bit-length of modulus.")
         }),
        "dsa_public_key":SubRecord({
            "p":IndexedBinary(),
            "q":IndexedBinary(),
            "g":IndexedBinary(),
            "y":IndexedBinary(),
        }),
        "ecdsa_public_key":SubRecord({
            "b":IndexedBinary(),
            "gx":IndexedBinary(),
            "gy":IndexedBinary(),
            "n":IndexedBinary(),
            "p":IndexedBinary(),
            "x":IndexedBinary(),
            "y":IndexedBinary(),
        })
    }),
    "extensions":SubRecord({
        "key_usage":SubRecord({
            "digital_signature":Boolean(),
            "certificate_sign":Boolean(),
            "crl_sign":Boolean(),
            "content_commitment":Boolean(),
            "key_encipherment":Boolean(),
            "value":Integer(), #we should document this. I don't know what this is.
            "data_encipherment":Boolean(),
            "key_agreement":Boolean(),
            "decipher_only":Boolean(),
            "encipher_only":Boolean(),
        }),
        "basic_constraints":SubRecord({
            "is_ca":Boolean(),
            "max_path_len":Integer(),
        }),
        "subject_alt_name":SubRecord({
            "dns_names":ListOf(AnalyzedString()),
            "email_addresses":ListOf(String()),
            "ip_addresses":ListOf(String()),
        }),
        "crl_distribution_points":ListOf(String()),
        "authority_key_id":Binary(),
        "subject_key_id":Binary(),
        "extended_key_usage":ListOf(Integer()),
        "certificate_policies":ListOf(AnalyzedString(es_include_raw=True)),
        "authority_info_access":SubRecord({
            "ocsp_urls":ListOf(AnalyzedString(es_include_raw=True)),
            "issuer_urls":ListOf(AnalyzedString(es_include_raw=True))
        }),
        "name_constraints":SubRecord({
            "critical":Boolean(),
            "permitted_names":ListOf(AnalyzedString(es_include_raw=True)),
        }),
    }),
    "unknown_extensions":ListOf(unknown_extension),
    "signature":SubRecord({
        "signature_algorithm":SubRecord({
            "name":String(),
            "oid":String(),
        }),
        "value":Binary(),
        "valid":Boolean(),
        "self_signed":Boolean(),
    }),
    "fingerprint_md5":String(),
    "fingerprint_sha1":String(),
    "fingerprint_sha256":String(),
})

zgrab_certificate = SubRecord({
    "parsed":zgrab_parsed_certificate
})

ztag_tls = SubRecord({
    "version":String(),
    "cipher_suite":SubRecord({
        "id":String(),
        "name":String(),
    }),
    "ocsp_stapling":Boolean(),
    "secure_renegotiation":Boolean(),
    "certificate":zgrab_certificate,
    "chain":ListOf(zgrab_certificate),
    "validation":SubRecord({
        "browser_trusted":Boolean(),
        "browser_error":AnalyzedString(es_include_raw=True),
        "matches_domain":Boolean(),
    }),
    "server_key_exchange":SubRecord({
        "ecdh_params":ztag_ecdh_params,
        "dh_params":ztag_dh_params,
        "rsa_params":ztag_rsa_params,
    }),
    "signature":SubRecord({
        "valid":Boolean(),
        "signature_error":AnalyzedString(es_include_raw=True),
        "signature_algorithm":String(), # prefer sig_and_hash, then fall back to proto-defined
        "hash_algorithm":String(), # prefer sig_and_hash, then fall back to proto-defined
    }),
    "metadata":local_metadata
})

ztag_sslv2 = SubRecord({
    "support": Boolean(),
    "extra_clear": Boolean(),
    "export": Boolean(),
    "certificate": zgrab_certificate,
    "ciphers": ListOf(SubRecord({
        "name": String(),
        "id": Integer(),
    })),
    "metadata": local_metadata,
})

ztag_heartbleed = SubRecord({
    "heartbeat_enabled":Boolean(),
    "heartbleed_vulnerable":Boolean(),
    "metadata":local_metadata
})

ztag_extended_random = SubRecord({
    "extended_random_support": Boolean(),
    "metadata":local_metadata
})

ztag_smtp_starttls = SubRecord({
    "banner": AnalyzedString(es_include_raw=True),
    "ehlo": AnalyzedString(es_include_raw=True),
    "starttls": AnalyzedString(es_include_raw=True),
    "tls": ztag_tls,
    "metadata":local_metadata
})

ztag_mail_starttls = SubRecord({
    "banner": AnalyzedString(es_include_raw=True),
    "starttls": AnalyzedString(es_include_raw=True),
    "tls": ztag_tls,
    "metadata":local_metadata
})

ztag_mail_tls = SubRecord({
    "tls":ztag_tls,
    "banner": AnalyzedString(es_include_raw=True),
    "metadata":local_metadata
})

zgrab_unknown_http_header = SubRecord({
    "key":AnalyzedString(es_include_raw=True),
    "value":AnalyzedString(es_include_raw=True)
})

zgrab_http_headers = SubRecord({
    "access_control_allow_origin":AnalyzedString(es_include_raw=True),
    "accept_patch":AnalyzedString(es_include_raw=True),
    "accept_ranges":AnalyzedString(es_include_raw=True),
    "age":AnalyzedString(es_include_raw=True),
    "allow":AnalyzedString(es_include_raw=True),
    "cache_control":AnalyzedString(es_include_raw=True),
    "connection":AnalyzedString(es_include_raw=True),
    "content_disposition":AnalyzedString(es_include_raw=True),
    "content_encoding":AnalyzedString(es_include_raw=True),
    "content_language":AnalyzedString(es_include_raw=True),
    "content_length":AnalyzedString(es_include_raw=True),
    "content_location":AnalyzedString(es_include_raw=True),
    "content_md5":AnalyzedString(es_include_raw=True),
    "content_range":AnalyzedString(es_include_raw=True),
    "content_type":AnalyzedString(es_include_raw=True),
    "date":AnalyzedString(es_include_raw=True),
    "etag":AnalyzedString(es_include_raw=True),
    "expires":AnalyzedString(es_include_raw=True),
    "last_modified":AnalyzedString(es_include_raw=True),
    "link":AnalyzedString(es_include_raw=True),
    "location":AnalyzedString(es_include_raw=True),
    "p3p":AnalyzedString(es_include_raw=True),
    "pragma":AnalyzedString(es_include_raw=True),
    "proxy_authenticate":AnalyzedString(es_include_raw=True),
    "public_key_pins":AnalyzedString(es_include_raw=True),
    "refresh":AnalyzedString(es_include_raw=True),
    "retry_after":AnalyzedString(es_include_raw=True),
    "server":AnalyzedString(es_include_raw=True),
    "set_cookie":AnalyzedString(es_include_raw=True),
    "status":AnalyzedString(es_include_raw=True),
    "strict_transport_security":AnalyzedString(es_include_raw=True),
    "trailer":AnalyzedString(es_include_raw=True),
    "transfer_encoding":AnalyzedString(es_include_raw=True),
    "upgrade":AnalyzedString(es_include_raw=True),
    "vary":AnalyzedString(es_include_raw=True),
    "via":AnalyzedString(es_include_raw=True),
    "warning":AnalyzedString(es_include_raw=True),
    "www_authenticate":AnalyzedString(es_include_raw=True),
    "x_frame_options":AnalyzedString(es_include_raw=True),
    "x_xss_protection":AnalyzedString(es_include_raw=True),
    "content_security_policy":AnalyzedString(es_include_raw=True),
    "x_content_security_policy":AnalyzedString(es_include_raw=True),
    "x_webkit_csp":AnalyzedString(es_include_raw=True),
    "x_content_type_options":AnalyzedString(es_include_raw=True),
    "x_powered_by":AnalyzedString(es_include_raw=True),
    "x_ua_compatible":AnalyzedString(es_include_raw=True),
    "x_content_duration":AnalyzedString(es_include_raw=True),
    "x_real_ip":String(doc="overloaded X-Real-IP in our proxy testing so that "\
                           "our scanner can detect who made the request."),
    "proxy_agent":AnalyzedString(es_include_raw=True),
    "unknown":ListOf(zgrab_unknown_http_header)
})

ztag_http = SubRecord({
    "status_code":Integer(),
    "status_line":AnalyzedString(es_include_raw=True),
    "body":HTML(),
    "headers":zgrab_http_headers,
    "body_sha256":String(),
    "title":AnalyzedString(es_include_raw=True),
    "metadata":local_metadata
})

ztag_open_proxy = SubRecord({
    "connect":SubRecord({
      "status_code":Integer(),
      "status_line":AnalyzedString(es_include_raw=True),
      "body":AnalyzedString(),
      "headers":zgrab_http_headers
    }),
    "get":SubRecord({
      "status_code":Integer(),
      "status_line":AnalyzedString(es_include_raw=True),
      "body":AnalyzedString(),
      "headers":zgrab_http_headers,
      "random_present":Boolean(),
      "body_sha256":String()
    }),
    "metadata":local_metadata
})

ztag_ssh_banner = SubRecord({
    "raw_banner": AnalyzedString(es_include_raw=True),
    "protocol_version": String(),
    "software_version": String(),
    "comment": String(),
    "metadata":local_metadata
})

ztag_ftp = SubRecord({
    "banner":AnalyzedString(es_include_raw=True),
    "metadata":local_metadata
})

telnet_caps_list = ListOf(SubRecord({
    "name":String(),
    "value":Integer()
}))

ztag_telnet = SubRecord({
    "banner":AnalyzedString(es_include_raw=True),
    "will":telnet_caps_list,
    "wont":telnet_caps_list,
    "do":telnet_caps_list,
    "dont":telnet_caps_list,
    "metadata":local_metadata
})

ztag_modbus = SubRecord({
    "function_code":Integer(),
    "mei_response":SubRecord({
      "conformity_level":Integer(),
      "objects":SubRecord({
        "vendor":AnalyzedString(es_include_raw=True),
        "product_code":AnalyzedString(es_include_raw=True),
        "revision":String(),
        "vendor_url":String(),
        "product_name":AnalyzedString(es_include_raw=True),
        "model_name":AnalyzedString(es_include_raw=True),
        "user_application_name":AnalyzedString(es_include_raw=True),
      })
    }),
    "metadata":local_metadata
})

ztag_bacnet = SubRecord({
    "instance_number": Integer(),
    "vendor": SubRecord({
        "id": Integer(),
        "reported_name": AnalyzedString(es_include_raw=True),
        "official_name": AnalyzedString(es_include_raw=True),
    }),
    "firmware_revision": String(),
    "application_software_revision": String(),
    "object_name": AnalyzedString(es_include_raw=True),
    "model_name": AnalyzedString(es_include_raw=True),
    "description": AnalyzedString(es_include_raw=True),
    "location": AnalyzedString(es_include_raw=True),
})

ztag_dns_question = SubRecord({
    "name":String(),
    "type":String()
})


ztag_dns_answer = SubRecord({
    "name":String(),
    "response":AnalyzedString(es_include_raw=True),
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
    "metadata":local_metadata
})

ztag_tls_support = SubRecord({
    "support": Boolean(),
    "metadata":local_metadata
})

ztag_fox = SubRecord({
    "version": AnalyzedString(es_include_raw=True),
    "id": Integer(),
    "hostname": AnalyzedString(es_include_raw=True),
    "host_address": AnalyzedString(es_include_raw=True),
    "app_name": AnalyzedString(es_include_raw=True),
    "app_version": AnalyzedString(es_include_raw=True),
    "vm_name": AnalyzedString(es_include_raw=True),
    "vm_version":AnalyzedString(es_include_raw=True),
    "os_name": AnalyzedString(es_include_raw=True),
    "os_version": AnalyzedString(es_include_raw=True),
    "station_name":AnalyzedString(es_include_raw=True),
    "language": AnalyzedString(es_include_raw=True),
    "time_zone": AnalyzedString(es_include_raw=True),
    "host_id": AnalyzedString(es_include_raw=True),
    "vm_uuid": AnalyzedString(es_include_raw=True),
    "brand_id": AnalyzedString(es_include_raw=True),
    "sys_info": AnalyzedString(es_include_raw=True),
    "auth_agent_type": String()
})

ztag_dnp3 = SubRecord({
    "support":Boolean(),
    "raw_response":Binary()
})

ztag_s7 = SubRecord({
    "support":Boolean(),
    "system":AnalyzedString(es_include_raw=True),
    "module":AnalyzedString(es_include_raw=True),
    "plant_id":AnalyzedString(es_include_raw=True),
    "copyright":AnalyzedString(es_include_raw=True),
    "serial_number":AnalyzedString(es_include_raw=True),
    "reserved_for_os":AnalyzedString(es_include_raw=True),
    "module_type":AnalyzedString(es_include_raw=True),
    "memory_serial_number":AnalyzedString(es_include_raw=True),
    "cpu_profile":AnalyzedString(es_include_raw=True),
    "oem_id":AnalyzedString(es_include_raw=True),
    "location":AnalyzedString(es_include_raw=True),
    "module_id":AnalyzedString(es_include_raw=True),
    "hardware":AnalyzedString(es_include_raw=True),
    "firmware":AnalyzedString(es_include_raw=True),
})

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
    ("ztag_sslv2", ztag_sslv2),
    ("ztag_sslv3", ztag_tls_support),
    ("ztag_tls1", ztag_tls_support),
    ("ztag_tls2", ztag_tls_support),
    ("ztag_tls3", ztag_tls_support),
    ("ztag_open_proxy", ztag_open_proxy),
    ("ztag_modbus", ztag_modbus),
    ("ztag_extended_random", ztag_extended_random),
    ("ztag_ssh_banner", ztag_ssh_banner),
    ("ztag_dns_lookup", ztag_dns_lookup),
    ("ztag_bacnet", ztag_bacnet),
    ("ztag_fox", ztag_fox),
    ("ztag_dnp3", ztag_dnp3),
    ("ztag_s7", ztag_s7),
]
for (name, schema) in ztag_schemas:
    x = Record({
        "ip_address":IPv4Address(required=True),
        "timestamp":DateTime(required=True),
        "tags":ListOf(String()),
        "metadata": SubRecord({}, allow_unknown=True),
    }, extends=schema)
    zschema.registry.register_schema("%s" % name, x)


ztag_hackingteam = SubRecord({
    "consistent":Boolean(),
    "response":AnalyzedString(es_include_raw=True),
})

ztag_lookup_spf = SubRecord({
    "raw":AnalyzedString(es_include_raw=True),
})

ztag_lookup_dmarc = SubRecord({
    "raw":AnalyzedString(es_include_raw=True),
    "p":String(),
})

ztag_lookup_axfr = SubRecord({
    "servers":ListOf(SubRecord{
        "ns":AnalyzedString(es_include_raw=True),
        "axfr":Boolean(),
        "error":AnalyzedString(es_include_raw=True),
        "records":ListOf(SubRecord({
            "name":AnalyzedString(es_include_raw=True),
            "ttl":Integer(),
            "rdclass":Integer(),
            "rdtype":Integer(),
            "rdata":AnalyzedString(es_include_raw=True),
            "pretty_rdclass":String(),
            "pretty_rdtype":String(),
            "pretty_name":AnalyzedString(es_include_raw=True),
        })
    }),
    "support":Boolean()
})

zdb_location = SubRecord({
    "continent":String(),
    "country":AnalyzedString(es_include_raw=True),
    "country_code":String(),
    "city":String(),
    "postal_code":String(),
    "timezone":String(),
    "province":AnalyzedString(es_include_raw=True),
    "latitude":Double(),
    "longitude":Double(),
    "registered_country":AnalyzedString(es_include_raw=True),
    "registered_country_code":String(),
})

zdb_as = SubRecord({
    "asn":Integer(),
    "description":AnalyzedString(es_include_raw=True),
    "path":ListOf(Integer()),
    "rir":String(),
    "routed_prefix":String(),
    "name":AnalyzedString(es_include_raw=True),
    "country_code":String(),
    "organization":AnalyzedString(es_include_raw=True)
})


__metadata = {}
for key in Annotation.GLOBAL_METADATA_KEYS:
    __metadata[key] = AnalyzedString(es_include_raw=True)
zdb_metadata = SubRecord(__metadata)

certificate = Record({
    "updated_at":DateTime(),
    "parsed":zgrab_parsed_certificate,
    "raw":Binary(),
    "tags":ListOf(AnalyzedString(es_include_raw=True)),
    "metadata":zdb_metadata,
    "parents":ListOf(String()),
    "validation_timestamp":DateTime(),
    "valid_nss": Boolean(),
    "valid_microsoft": Boolean(),
    "valid_apple": Boolean(),
})

zschema.registry.register_schema("certificate", certificate)

cryptkey = Record({

})


host = Record({
            Port(443):SubRecord({
                "https":SubRecord({
                    "tls":ztag_tls,
                    "heartbleed":ztag_heartbleed,
                    "dhe": ztag_dh,
                    "export_rsa": ztag_rsa_export,
                    "export_dhe": ztag_dh_export,
                    "ssl_2": ztag_sslv2,
                    "tls_1_1": ztag_tls_support,
                    "tls_1_2": ztag_tls_support,
                    "tls_1_3": ztag_tls_support,
                    "ecdhe": ztag_ecdh,
                    "open_proxy":ztag_open_proxy,
                    "extended_random":ztag_extended_random,
                })
            }),
            Port(80):SubRecord({
                "http":SubRecord({
                    "get":ztag_http,
                    "hackingteam":ztag_hackingteam, #TODO: zakir add private tag to schema
                    "open_proxy":ztag_open_proxy
                }),
            }),
            Port(25):SubRecord({
                "smtp":SubRecord({
                    "starttls": ztag_smtp_starttls,
                    "ssl_2": ztag_sslv2,
                }),
            }),
            Port(23):SubRecord({
                "telnet":SubRecord({
                    "banner":ztag_telnet
                })
            }),
            Port(21):SubRecord({
                "ftp":SubRecord({
                  "banner":ztag_ftp,
                })
            }),
            Port(102):SubRecord({
                "s7":SubRecord({
                    "szl":ztag_s7
                })
            }),
            Port(110):SubRecord({
                "pop3":SubRecord({
                    "starttls":ztag_mail_starttls,
                    "ssl_2": ztag_sslv2,
                })
            }),
            Port(143):SubRecord({
                "imap":SubRecord({
                    "starttls":ztag_mail_starttls,
                    "ssl_2": ztag_sslv2,
                })
            }),
            Port(993):SubRecord({
                "imaps":SubRecord({
                    "tls":ztag_mail_tls,
                    "ssl_2": ztag_sslv2,
                })
            }),
            Port(995):SubRecord({
                "pop3s":SubRecord({
                    "tls":ztag_mail_tls,
                    "ssl_2": ztag_sslv2,
                })
            }),
            Port(587):SubRecord({
                "smtp":SubRecord({
                    "starttls": ztag_smtp_starttls,
                    "ssl_2": ztag_sslv2,
                })
            }),
            Port(502):SubRecord({
                "modbus":SubRecord({
                    "device_id":ztag_modbus
                })
            }),
            Port(22):SubRecord({
                "ssh":SubRecord({
                    "banner": ztag_ssh_banner
                }),
            }),
            Port(53):SubRecord({
                "dns":SubRecord({
                    "lookup":ztag_dns_lookup
                })
            }),
            Port(47808):SubRecord({
                "bacnet":SubRecord({
                    "device_id":ztag_bacnet
                })
            }),
            Port(1911):SubRecord({
                "fox":SubRecord({
                    "device_id":ztag_fox
                })
            }),
            Port(20000):SubRecord({
                "dnp3":SubRecord({
                    "status":ztag_dnp3,
                })
            }),
            "tags":ListOf(AnalyzedString(es_include_raw=True)),
            "metadata":zdb_metadata,
            "location":zdb_location,
            "__restricted_location":zdb_location,
            "autonomous_system":zdb_as,
            "notes":EnglishString(es_include_raw=True),
            "ip":IPv4Address(required=True),
            "ipint":Long(required=True, doc="Integer value of IP address in host order"),
            "domain":String(),
            "alexa_rank":Integer(doc="Rank in the Alexa Top 1 Million. "
                    "Null if not currently in the Top 1 Million sites."),
            "updated_at":DateTime(),
            "zdb_version":Integer(),
            "protocols":ListOf(String())
})

domain = Record({
            Port(443):SubRecord({
                "https":SubRecord({
                    "tls":ztag_tls,
                    "heartbleed":ztag_heartbleed,
                    "dhe": ztag_dh,
                    "export_rsa": ztag_rsa_export,
                    "export_dhe": ztag_dh_export,
                    "tls_1_1": ztag_tls_support,
                    "tls_1_2": ztag_tls_support,
                    "tls_1_3": ztag_tls_support,
                    "ecdhe": ztag_ecdh,
                    "open_proxy":ztag_open_proxy,
                    "extended_random":ztag_extended_random,
                })
            }),
            Port(80):SubRecord({
                "http":SubRecord({
                    "get":ztag_http,
                    "hackingteam":ztag_hackingteam, #TODO: zakir add private tag to schema
                    "open_proxy":ztag_open_proxy
                }),
            }),
            Port(25):SubRecord({
                "smtp":SubRecord({
                    "starttls": ztag_smtp_starttls,
                })
            }),
            Port(23):SubRecord({
                "telnet":SubRecord({
                    "banner":ztag_telnet
                })
            }),
            Port(21):SubRecord({
                "ftp":SubRecord({
                  "banner":ztag_telnet
                })
            }),
            Port(102):SubRecord({
                "s7":SubRecord({
                    "szl":ztag_s7
                })
            }),
            Port(110):SubRecord({
                "pop3":SubRecord({
                  "starttls":ztag_mail_starttls
                })
            }),
            Port(143):SubRecord({
                "imap":SubRecord({
                    "starttls":ztag_mail_starttls
                })
            }),
            Port(993):SubRecord({
                "imaps":SubRecord({
                    "tls":ztag_mail_tls
                })
            }),
            Port(995):SubRecord({
                "pop3s":SubRecord({
                    "tls":ztag_mail_tls
                })
            }),
            Port(0):SubRecord({
                "lookup":SubRecord({
                    "spf":ztag_lookup_spf,
                    "dmarc":ztag_lookup_dmarc,
                    "axfr":ztag_lookup_axfr,
                })
            }),

            "tags":ListOf(AnalyzedString(es_include_raw=True)),
            "metadata":zdb_metadata,
            "location":zdb_location,
            "__restricted_location":zdb_location,
            "autonomous_system":zdb_as,
            "notes":EnglishString(es_include_raw=True),
            "domain":String(),
            "alexa_rank":Integer(doc="Rank in the Alexa Top 1 Million. "
                    "Null if not currently in the Top 1 Million sites."),
            "updated_at":DateTime(),
            "zdb_version":Integer(),
            "protocols":ListOf(String())
})


DROP_KEYS = {'ip_address', 'metadata', 'tags', 'timestamp'}

zschema.registry.register_schema("host", host)
