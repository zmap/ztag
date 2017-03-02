from zschema.leaves import *
from zschema.compounds import *

import zschema.registry

from ztag.annotation import Annotation


class CensysString(WhitespaceAnalyzedString):
    "default type for any strings in Censys"
    INCLUDE_RAW = True


__local_metadata = {}
for key in Annotation.LOCAL_METADATA_KEYS:
    __local_metadata[key] = CensysString()
local_metadata = SubRecord(__local_metadata)

zgrab_subj_issuer = SubRecord({
    "serial_number":ListOf(String()),
    "common_name":ListOf(CensysString()),
    "country":ListOf(CensysString()),
    "locality":ListOf(CensysString()),
    "province":ListOf(CensysString()),
    "street_address":ListOf(CensysString()),
    "organization":ListOf(CensysString()),
    "organizational_unit":ListOf(CensysString()),
    "postal_code":ListOf(String()),
    "domain_component":ListOf(CensysString()),
})

unknown_extension = SubRecord({
    "id":OID(),
    "critical":Boolean(),
    "value":IndexedBinary(),
})

edi_party_name = SubRecord({
    "name_assigner":CensysString(),
    "party_name":CensysString(),
})

alternate_name = SubRecord({
    "dns_names":ListOf(FQDN()),
    "email_addresses":ListOf(EmailAddress()),
    "ip_addresses":ListOf(IPAddress()),
    "directory_names":ListOf(zgrab_subj_issuer),
    "edi_party_names":ListOf(edi_party_name),
    "other_names":ListOf(SubRecord({
        "id":OID(),
        "value":IndexedBinary(),
    })),
    "registered_ids":ListOf(OID()),
    "uniform_resource_identifiers":ListOf(URI()),
})

ztag_dh_params = SubRecord({
    "prime":SubRecord({
        "value":IndexedBinary(),
        "length":Unsigned16BitInteger(),
    }),
    "generator":SubRecord({
        "value":IndexedBinary(),
        "length":Unsigned16BitInteger(),
    }),
})

ztag_dh_export = SubRecord({
    "dh_params":ztag_dh_params,
    "support":Boolean(),
    "metadata":local_metadata,
    "timestamp":DateTime(),
})

ztag_dh = SubRecord({
    "dh_params":ztag_dh_params,
    "support":Boolean(),
    "metadata":local_metadata,
    "timestamp":DateTime(),
})

ztag_rsa_params = SubRecord({
   "exponent":Unsigned32BitInteger(),
   "modulus":IndexedBinary(),
   "length":Unsigned16BitInteger(),
})

ztag_rsa_export = SubRecord({
    "rsa_params":ztag_rsa_params,
    "support":Boolean(),
    "metadata":local_metadata,
    "timestamp":DateTime(),
})

ztag_ecdh_params = SubRecord({
    "curve_id":SubRecord({
        "name":String(),
        "id":Unsigned16BitInteger(),
    })
})

ztag_ecdh = SubRecord({
    "ecdh_params":ztag_ecdh_params,
    "support":Boolean(),
    "metadata":local_metadata,
    "timestamp":DateTime(),
})

ztag_sct = SubRecord({
    "version":Unsigned8BitInteger(),
    "log_id":IndexedBinary(),
    "log_name":String(),
    "timestamp":DateTime(),
    "signature":Binary(),
    "extensions":Binary(),
})

expanded_cidr = SubRecord({
    "cidr":String(),
    "begin":IPAddress(),
    "end":IPAddress(),
    "mask":IPAddress(),
}, exclude=["bigquery",]) # XXX

certificate_policy = SubRecord({
    "id":OID(),
    "name":String(),
    "cps":ListOf(URL()),
    "user_notice":SubRecord({
        "explit_text":EnglishString(),
        "notice_reference":ListOf(SubRecord({
            "organization":CensysString(),
            "notice_numbers":ListOf(Signed32BitInteger())
        }))
    })
}, exclude=["bigquery",]) # XXX

zgrab_parsed_certificate = SubRecord({
    "subject":zgrab_subj_issuer,
    "subject_dn":CensysString(),
    "issuer":zgrab_subj_issuer,
    "issuer_dn":CensysString(),
    "version":Unsigned8BitInteger(),
    "serial_number":String(doc="Serial number as an signed decimal integer. "\
                               "Stored as string to support >uint lengths. "\
                               "Negative values are allowed."),
    "validity":SubRecord({
        "start":DateTime(doc="Timestamp of when certificate is first valid. Timezone is UTC."),
        "end":DateTime(doc="Timestamp of when certificate expires. Timezone is UTC."),
        "length":Signed64BitInteger(),
    }),
    "signature_algorithm":SubRecord({
        "name":String(),
        "oid":OID(),
    }),
    "subject_key_info":SubRecord({
        "fingerprint_sha256":HexString(),
        "key_algorithm":SubRecord({
            "name":String(doc="Name of public key type, e.g., RSA or ECDSA. "\
                              "More information is available the named SubRecord "\
                              "(e.g., rsa_public_key)."),
            "oid":OID(doc="OID of the public key on the certificate. "\
                             "This is helpful when an unknown type is present. "\
                             "This field is reserved and not current populated.")
         }),
        "rsa_public_key":SubRecord({
            "exponent":Unsigned32BitInteger(),
            "modulus":IndexedBinary(),
            "length":Unsigned16BitInteger(doc="Bit-length of modulus.")
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
            "pub":Binary(),
            "curve":Enum(),
            "length":Unsigned16BitInteger(),
            #"asn1_oid":OID(), # TODO: this is currently commented out
            # because for a bunch of certificates, this was encoded as [1, 2,
            # 840, 113549, 1, 1, 12] not 1.2.840.113549.1.1.12
        })
    }),
    "extensions":SubRecord({
        "key_usage":SubRecord({
            "value":Unsigned16BitInteger("Integer value of the bitmask in the extension"),
            "digital_signature":Boolean(),
            "certificate_sign":Boolean(),
            "crl_sign":Boolean(),
            "content_commitment":Boolean(),
            "key_encipherment":Boolean(),
            "data_encipherment":Boolean(),
            "key_agreement":Boolean(),
            "decipher_only":Boolean(),
            "encipher_only":Boolean(),
        }),
        "basic_constraints":SubRecord({
            "is_ca":Boolean(),
            "max_path_len":Signed32BitInteger(),
        }),
        "subject_alt_name":alternate_name,
        "issuer_alt_name":alternate_name,
        "crl_distribution_points":ListOf(URL()),
        "authority_key_id":HexString(),
        "subject_key_id":HexString(),
        "extended_key_usage":SubRecord({
            "value":ListOf(Signed32BitInteger()), # TODO: remove after reparse
            #"server_auth":Boolean(doc="TLS WWW server authentication"),
            #"client_auth":Boolean(doc="TLS WWW client authentication"),
            #"code_signing":Boolean(doc="Signing of downloadable executable code"),
            #"email_protection":Boolean(doc="Email protection"),
            #"time_stamping":Boolean(doc="Binding the hash of an object to a time"),
            #"ocsp_signing":Boolean(doc="Signing OCSP responses"),
            #"unknown":ListOf(OID)
        }, exclude=["bigquery",]), # XXX
        "certificate_policies":ListOf(certificate_policy),
        "authority_info_access":SubRecord({
            "ocsp_urls":ListOf(URL()),
            "issuer_urls":ListOf(URL())
        }),
        "name_constraints":SubRecord({
            "critical":Boolean(),
            "permitted_names":ListOf(FQDN()),
            # We do not schema email addresses as an EmailAddress per
            # rfc5280#section-4.2.1.10 documnetation:
            # A name constraint for Internet mail addresses MAY specify a
            # particular mailbox, all addresses at a particular host, or all
            # mailboxes in a domain.  To indicate a particular mailbox, the
            # constraint is the complete mail address.  For example,
            # "root@example.com" indicates the root mailbox on the host
            # "example.com".  To indicate all Internet mail addresses on a
            # particular host, the constraint is specified as the host name.  For
            # example, the constraint "example.com" is satisfied by any mail
            # address at the host "example.com".  To specify any address within a
            # domain, the constraint is specified with a leading period (as with
            # URIs).  For example, ".example.com" indicates all the Internet mail
            # addresses in the domain "example.com", but not Internet mail
            # addresses on the host "example.com".
            "permitted_email_addresses":ListOf(CensysString()),
            "permitted_ip_addresses":ListOf(expanded_cidr),
            "permitted_directory_names":ListOf(zgrab_subj_issuer),
            "permitted_registered_ids":ListOf(OID()),
            "permitted_edi_party_names":ListOf(edi_party_name),
            "excluded_names":ListOf(FQDN()),
            "excluded_email_addresses":ListOf(CensysString()),
            "excluded_ip_addresses":ListOf(expanded_cidr),
            "excluded_directory_names":ListOf(zgrab_subj_issuer),
            "excluded_registered_ids":ListOf(OID()),
            "excluded_edi_party_names":ListOf(edi_party_name),

        }),
        "signed_certificate_timestamps":ListOf(ztag_sct),
        "ct_poison":Boolean()
    }),
    "unknown_extensions":ListOf(unknown_extension),
    "signature":SubRecord({
        "signature_algorithm":SubRecord({
            "name":String(),
            "oid":OID(),
        }),
        "value":IndexedBinary(),
        "valid":Boolean(),
        "self_signed":Boolean(),
    }),
    "fingerprint_md5":HexString(),
    "fingerprint_sha1":HexString(),
    "fingerprint_sha256":HexString(),
    "spki_subject_fingerprint":HexString(),
    "tbs_fingerprint":HexString(),
    "tbs_noct_fingerprint":HexString(),
    "names":ListOf(FQDN()),
    "validation_level":Enum(),
    "redacted":Boolean(),
})

zgrab_certificate_trust = SubRecord({
    "type":Enum(doc="root, intermediate, or leaf certificate"),
    "trusted_path":Boolean(doc="Does certificate chain up to browser root store"),
    "valid":Boolean(doc="is this certificate currently valid in this browser"),
    "was_valid":Boolean(doc="was this certificate ever valid in this browser")
})

zgrab_certificate = SubRecord({
    "parsed":zgrab_parsed_certificate,
    "validation":SubRecord({
        "nss":zgrab_certificate_trust,
        "apple":zgrab_certificate_trust,
        "microsoft":zgrab_certificate_trust,
        "android":zgrab_certificate_trust,
        "java":zgrab_certificate_trust,
    }),
})


zgrab_server_certificate_valid = SubRecord({
    "complete_chain":Boolean(doc="does server provide a chain up to a root"),
    "valid":Boolean(doc="is this certificate currently valid in this browser"),
    "error":CensysString()
})

ztag_tls = SubRecord({
    "version":String(),
    "cipher_suite":SubRecord({
        "id":String(),
        "name":CensysString(),
    }),
    "ocsp_stapling":Boolean(),
    "secure_renegotiation":Boolean(),
    "certificate":zgrab_certificate,
    "chain":ListOf(zgrab_certificate),
    "scts":ListOf(ztag_sct),
    "session_ticket":SubRecord({
        "length":Unsigned32BitInteger(),
        "lifetime_hint":Unsigned32BitInteger(),
    }),
    "validation":SubRecord({
        "matches_domain":Boolean(),
        "browser_trusted":Boolean(),
        #"stores":SubRecord({
        #    "nss":zgrab_server_certificate_valid,
        #    "microsoft":zgrab_server_certificate_valid,
        #    "apple":zgrab_server_certificate_valid,
        #    "java":zgrab_server_certificate_valid,
        #    "android":zgrab_server_certificate_valid,
        #})
    }),
    "server_key_exchange":SubRecord({
        "ecdh_params":ztag_ecdh_params,
        "dh_params":ztag_dh_params,
        "rsa_params":ztag_rsa_params,
    }),
    "signature":SubRecord({
        "valid":Boolean(),
        "signature_error":CensysString(),
        "signature_algorithm":CensysString(), # prefer sig_and_hash, then fall back to proto-defined | TODO: does this meet our needs?
        "hash_algorithm":CensysString(), # prefer sig_and_hash, then fall back to proto-defined | TODO: does this meet our needs?
    }),
    "metadata":local_metadata,
    "timestamp":DateTime(),
})

ztag_sslv2 = SubRecord({
    "support": Boolean(),
    "extra_clear": Boolean(),
    "export": Boolean(),
    "certificate": zgrab_certificate,
    "ciphers": ListOf(SubRecord({
        "name": String(),
        "id": Unsigned32BitInteger(),
    })),
    "metadata": local_metadata,
    "timestamp":DateTime(),
})

ztag_heartbleed = SubRecord({
    "heartbeat_enabled":Boolean(),
    "heartbleed_vulnerable":Boolean(),
    "metadata":local_metadata,
    "timestamp":DateTime(),
})

ztag_extended_random = SubRecord({
    "extended_random_support": Boolean(),
    "metadata":local_metadata,
    "timestamp":DateTime(),
})

ztag_smtp_starttls = SubRecord({
    "banner": CensysString(),
    "ehlo": CensysString(),
    "starttls": CensysString(),
    "tls": ztag_tls,
    "metadata":local_metadata,
    "timestamp":DateTime(),
})

ztag_mail_starttls = SubRecord({
    "banner": CensysString(),
    "starttls": CensysString(),
    "tls": ztag_tls,
    "metadata":local_metadata,
    "timestamp":DateTime(),
})

ztag_mail_tls = SubRecord({
    "tls":ztag_tls,
    "banner": CensysString(),
    "metadata":local_metadata,
    "timestamp":DateTime(),
})

zgrab_unknown_http_header = SubRecord({
    "key":String(),
    "value":CensysString()
})

zgrab_http_headers = SubRecord({
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
    #"referer":CensysString(), // TODO: Why is this commented out?
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
    #"x_real_ip":CensysString(doc="overloaded X-Real-IP in our proxy testing so that "\
    #                       "our scanner can detect who made the request."),
    "proxy_agent":CensysString(),
    "unknown":ListOf(zgrab_unknown_http_header)
})

ztag_http = SubRecord({
    "status_code":Unsigned16BitInteger(),
    "status_line":CensysString(),
    "body":HTML(),
    "headers":zgrab_http_headers,
    "body_sha256":HexString(),
    "title":CensysString(),
    "metadata":local_metadata,
    "timestamp":DateTime(),
})

#ztag_open_proxy = SubRecord({
#    "connect":SubRecord({
#      "status_code":Integer(),
#      "status_line":CensysString(),
#      "body":CensysString(),
#      "headers":zgrab_http_headers
#    }),
#    "get":SubRecord({
#      "status_code":Integer(),
#      "status_line":CensysString(),
#      "body":CensysString(),
#      "headers":zgrab_http_headers,
#      "random_present":Boolean(),
#      "body_sha256":HexString()
#    }),
#    "metadata":local_metadata
#})

ztag_ssh_banner = SubRecord({
    "raw_banner":CensysString(),
    "protocol_version":String(),
    "software_version":String(),
    "comment":CensysString(),
    "metadata":local_metadata,
    "timestamp":DateTime(),
})

ztag_ftp = SubRecord({
    "banner":CensysString(),
    "metadata":local_metadata,
    "timestamp":DateTime(),
})

telnet_caps_list = ListOf(SubRecord({
    "name":String(),
    "value":Unsigned32BitInteger()
}))

ztag_telnet = SubRecord({
    "support":Boolean(),
    "banner":CensysString(),
    "will":telnet_caps_list,
    "wont":telnet_caps_list,
    "do":telnet_caps_list,
    "dont":telnet_caps_list,
    "metadata":local_metadata,
    "timestamp":DateTime(),
})

ztag_modbus = SubRecord({
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
    "timestamp":DateTime(),
})

ztag_bacnet = SubRecord({
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
    "timestamp":DateTime(),
})

ztag_dns_question = SubRecord({
    "name":String(),
    "type":String()
})


ztag_dns_answer = SubRecord({
    "name":String(),
    "response":CensysString(),
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
    "timestamp":DateTime(),
})

ztag_tls_support = SubRecord({
    "support": Boolean(),
    "metadata":local_metadata,
    "timestamp":DateTime(),
})

ztag_fox = SubRecord({
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
    "timestamp":DateTime(),
})

ztag_dnp3 = SubRecord({
    "support":Boolean(),
    "raw_response":Binary(),
    "metadata":local_metadata,
    "timestamp":DateTime(),
})

ztag_s7 = SubRecord({
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
    "timestamp":DateTime(),
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
    #("ztag_open_proxy", ztag_open_proxy),
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
        #"timestamp":DateTime(required=True),
        "tags":ListOf(String()),
        "metadata": SubRecord({}, allow_unknown=True),
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
zdb_metadata = SubRecord(__metadata)

CTServerStatus = SubRecord({
    "index":Signed64BitInteger(),
    "added_to_ct_at":DateTime(),
    "ct_to_censys_at":DateTime(),
    "censys_to_ct_at":DateTime(),
    "sct":Binary(),
})

CTStatus = SubRecord({

    "censys_dev":CTServerStatus,
    "censys":CTServerStatus,

    "google_aviator":CTServerStatus,
    "google_pilot":CTServerStatus,
    "google_rocketeer":CTServerStatus,
    "google_submariner":CTServerStatus,
    "google_testtube":CTServerStatus,
    "google_skydiver":CTServerStatus,
    "google_icarus":CTServerStatus,
    "google_daedalus":CTServerStatus,

    "comodo_dodo":CTServerStatus,
    "comodo_mammoth":CTServerStatus,

    "digicert_ct1":CTServerStatus,
    "izenpe_com_ct":CTServerStatus,
    "izenpe_eus_ct":CTServerStatus,
    "symantec_ws_ct":CTServerStatus,
    "symantec_ws_vega":CTServerStatus,
    "symantec_ws_sirius":CTServerStatus,
    "wosign_ctlog":CTServerStatus,
    "wosign_ct":CTServerStatus,
    "cnnic_ctserver":CTServerStatus,
    "gdca_ct":CTServerStatus,
    "gdca_ctlog":CTServerStatus,
    "startssl_ct":CTServerStatus,
    "certly_log":CTServerStatus,
    "venafi_api_ctlog":CTServerStatus,
    "symantec_ws_deneb":CTServerStatus,
    "nordu_ct_plausible":CTServerStatus,
})

CertificateAudit = SubRecord({
    "nss":SubRecord({
        "current_in":Boolean(),
        "was_in":Boolean(),
        "owner_name":CensysString(),
        "parent_name":CensysString(),
        "certificate_name":CensysString(),
        "certificate_policy":CensysString(),
        "certification_practice_statement":CensysString(),
        "cp_same_as_parent":CensysString(),
        "audit_same_as_parent":CensysString(),
        "standard_audit":CensysString(),
        "br_audit":CensysString(),
        "auditor":CensysString(),
        "standard_audit_statement_timestamp":DateTime(),
        "management_assertions_by":CensysString(),
     })
})

ztag_certificate_validation = SubRecord({
    "valid":Boolean(),
    "was_valid":Boolean(),
    "trusted_path":Boolean(),
    "was_trusted_path":Boolean(),
    "blacklisted":Boolean(),
    "type":Enum(["leaf","intermediate","root"]),
})

certificate = Record({
    "updated_at":DateTime(),
    "parsed":zgrab_parsed_certificate,
    "raw":Binary(),
    "tags":ListOf(CensysString()),
    "metadata":zdb_metadata,
    "parents":ListOf(String()),
    "validation_timestamp":DateTime(),
    ## TODO: DEPRECATED validation. These should be removed in the future:
    "valid_nss": Boolean(deprecated=True),
    "was_valid_nss":Boolean(deprecated=True),
    "current_valid_nss":Boolean(deprecated=True),
    "in_nss":Boolean(deprecated=True),
    "current_in_nss":Boolean(deprecated=True),
    "was_in_nss":Boolean(deprecated=True),
    ## new style validation
    "validation":SubRecord({
        "nss":ztag_certificate_validation,
        "apple":ztag_certificate_validation,
        "microsoft":ztag_certificate_validation,
        "java":ztag_certificate_validation,
        "android":ztag_certificate_validation,
        "google_ct_primary":ztag_certificate_validation,
        "google_ct_submariner":ztag_certificate_validation,
    }),
    "revoked":Boolean(doc="reserved"),
    "ct":CTStatus,
    "seen_in_scan":Boolean(),
    "source":String(),
    "audit":CertificateAudit,
    "precert":Boolean(),
})

zschema.registry.register_schema("certificate", certificate)

cryptkey = Record({

})


ipv4_host = Record({
            Port(443):SubRecord({
                "https":SubRecord({
                    "tls":ztag_tls,
                    "heartbleed":ztag_heartbleed,
                    "dhe": ztag_dh,
                    "rsa_export": ztag_rsa_export,
                    "dhe_export": ztag_dh_export,
                    "ssl_2": ztag_sslv2,
                    "tls_1_1": ztag_tls_support,
                    "tls_1_2": ztag_tls_support,
                    #"tls_1_3": ztag_tls_support,
                    "ecdhe": ztag_ecdh,
                    #"extended_random":ztag_extended_random,
                })
            }),
            Port(80):SubRecord({
                "http":SubRecord({
                    "get":ztag_http,
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
            Port(7547):SubRecord({
                "cwmp":SubRecord({
                    "get":ztag_http,
                })
            }),

            "tags":ListOf(CensysString()),
            "metadata":zdb_metadata,
            "location":zdb_location,
            "__restricted_location":zdb_restricted_location,
            "autonomous_system":zdb_as,
            "notes":CensysString(),
            "ip":IPv4Address(required=True),
            "ipint":Unsigned32BitInteger(required=True, doc="Integer value of IP address in host order"),
            "updated_at":DateTime(),
            "zdb_version":Unsigned32BitInteger(),
            "protocols":ListOf(CensysString(exclude=["bigquery"]))
})

website = Record({
            Port(443):SubRecord({
                "https":SubRecord({
                    "tls":ztag_tls,
                    "heartbleed":ztag_heartbleed,
                    "dhe": ztag_dh,
                    "export_rsa": ztag_rsa_export,
                    "export_dhe": ztag_dh_export,
                    "tls_1_1": ztag_tls_support,
                    "tls_1_2": ztag_tls_support,
                    "ecdhe": ztag_ecdh,
                })
            }),
            Port(80):SubRecord({
                "http":SubRecord({
                    "get":ztag_http,
                }),
            }),
            Port(25):SubRecord({
                "smtp":SubRecord({
                    "starttls": ztag_smtp_starttls,
                })
            }),
            Port(0):SubRecord({
                "lookup":SubRecord({
                    "spf":ztag_lookup_spf,
                    "dmarc":ztag_lookup_dmarc,
                    "axfr":ztag_lookup_axfr,
                })
            }),

            "tags":CensysString(),
            "metadata":zdb_metadata,
            "notes":EnglishString(es_include_raw=True),
            "domain":String(),
            "alexa_rank":Unsigned32BitInteger(doc="Rank in the Alexa Top 1 Million. "
                    "Null if not currently in the Top 1 Million sites."),
            "updated_at":DateTime(),
            "zdb_version":Unsigned32BitInteger(),
            "protocols":ListOf(String())
})


DROP_KEYS = {'ip_address', 'metadata', 'tags', 'timestamp'}

zschema.registry.register_schema("ipv4host", ipv4_host)
zschema.registry.register_schema("website", website)
