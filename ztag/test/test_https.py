import base64
import logging
import random
import sys
import unittest
import json
import os.path

from ztag import protocols
from ztag.stream import Stream, Outgoing
from ztag.transforms import HTTPTransform, HTTPSGetTransform
import re

logging.basicConfig(stream=sys.stderr)

logger = logging.getLogger(__file__)
logger.trace = logger.debug
logger.setLevel(5)


def get_fake_cert(cert_id):
    return {
        "parsed": {
            "fingerprint_sha256": "PARSED_CERT_" + cert_id
        },
        "raw": "RAW_CERT_" + cert_id
    }


def get_expected_cert(cert_id):
    return {
        "parsed": {
            "fingerprint_sha256": "PARSED_CERT_" + cert_id,
        },
    }


def get_tls_handshake(cert_id):
    return {
        "server_hello": {
            "version": {
                "name": "TLS_VERSION"
            }
        },
        "server_certificates": {
            "certificate": get_fake_cert(cert_id + "_END_ENTITY"),
            "chain": [
                get_fake_cert(cert_id + "_CHAIN_0"),
                get_fake_cert(cert_id + "_CHAIN_1"),
            ]
        },
    }


def get_fake_sha256(body):
    return "SHA256(" + body + ")"


def get_http_response(body="body", tls=None):
    ret = {
        "status_line": "200 OK",
        "status_code": 200,
        "body": body,
        "body_sha256": get_fake_sha256(body),
        "headers": {},
        "request": {}
    }
    if tls is not None:
        ret["request"]["tls_handshake"] = get_tls_handshake(tls)

    return ret


def get_zgrab_http_response(ip, timestamp="now", body="body", error=None, tls=None, chain=None):
    if error is not None:
        return {
            "data": {
                "http": {
                    "error_component": error
                }
            }
        }

    return {
        "ip": ip,
        "timestamp": timestamp,
        "data": {
            "http": {
                "response": get_http_response(body, tls),
                "redirect_response_chain": [
                    get_http_response(body=entry.get("body"), tls=entry.get("tls"))
                    for entry in (chain or [])
                ]
            }
        }
    }


def get_expected_tls(cert_id):
    return {
        "version":  "TLS_VERSION",
        "certificate": get_expected_cert(cert_id + "_END_ENTITY"),
        "chain": [
            get_expected_cert(cert_id + "_CHAIN_0"),
            get_expected_cert(cert_id + "_CHAIN_1"),
        ],
    }


class Accumulator(Outgoing):
    def __init__(self):
        self.output = [];

    def take(self, obj):
        self.output.append(obj)

    def __len__(self):
        return len(self.output)

    def __iter__(self):
        return self.output.__iter__()


def get_expected_output(ip, timestamp="now", body="body", error=None, tls=None, chain=None):
    ret = {
        "body": body,
        "status_code": 200,
        "tags": [
            "http"
        ],
        "status_line": "200 OK",
        "global_metadata": {},
        "body_sha256":  get_fake_sha256(body),
        "timestamp": timestamp,
        "ip_address": ip,
        "local_metadata": {}
    }
    all_tls = [e.get("tls") for e in (chain or [])] + [tls]
    if all_tls[0] is not None:
        ret["tls_initial"] = get_expected_tls(all_tls[0])
    if all_tls[-1] is not None:
        ret["tls"] = get_expected_tls(all_tls[-1])
    return ret


class HTTPSTaggingTestCase(unittest.TestCase):
    """
    Check that whether the initial scan is HTTP or HTTPS, the result ends up tagged as "http", and
    that the initial / final TLS handshakes, if present, are included. Checks the case where there
    are no redirects, where there is a single redirect (https->https, http->http, https->http,
    http->https), and where there are two redirects (all cases except http->https->https and https->
    http->http).
    """
    CASES = {
        "no_tls_no_redirect": {
            "ip": "1.0.0.1",
            "body": "no TLS, no redirect",
            "tls": None,
        },
        "tls_no_redirect": {
            "ip": "1.0.1.1",
            "body": "TLS, no redirect",
            "tls": "tls_no_redirect",
        },
        "one_redirect_no_tls": {
            "ip": "1.0.2.1",
            "body": "single redirect, no TLS anywhere",
            "chain": [
                {
                    "ip": "1.0.2.2",
                    "body": "first target for 1.0.2.1 scan",
                }
            ]
        },
        "one_redirect_http_to_https": {
            "ip": "1.0.3.1",
            "body": "single redirect: from HTTP to HTTPS",
            "tls": "one_redirect_http_to_https",
            "chain": [
                {
                    "ip": "1.0.3.2",
                    "body": "this was just HTTP, but redirects to HTTPS"
                }
            ]
        },
        "one_redirect_https_to_http": {
            "ip": "1.0.4.1",
            "body": "single redirect: from HTTPS to HTTP",
            "chain": [
                {
                    "ip": "1.0.4.2",
                    "body": "this was HTTPS, but redirects to HTTP",
                    "tls": "one_redirect_https_to_http",
                }
            ]
        },
        "one_redirect_all_tls": {
            "ip": "1.0.5.1",
            "body": "single redirect: from HTTPS to HTTPS",
            "tls": "one_redirect_all_tls",
            "chain": [
                {
                    "ip": "1.0.5.2",
                    "body": "this was HTTPS, redirects to HTTPS",
                    "tls": "one_redirect_all_tls",
                }
            ]
        },
        "two_redirects_all_tls": {
            "ip": "1.0.6.1",
            "body": "two redirects: all HTTPS",
            "tls": "two_redirects_all_tls",
            "chain": [
                {
                    "ip": "1.0.6.2",
                    "body": "this was HTTPS, redirects to HTTPS",
                    "tls": "two_redirects_all_tls_1",
                },
                {
                    "ip": "1.0.6.3",
                    "body": "this was HTTPS, redirects to HTTPS",
                    "tls": "two_redirects_all_tls_2",
                },

            ]
        },
        "two_redirects_https_via_http": {
            "ip": "1.0.7.1",
            "body": "two redirects: HTTPS via HTTP",
            "tls": "two_redirects_https_via_http",
            "chain": [
                {
                    "ip": "1.0.7.2",
                    "body": "First step: HTTPS",
                    "tls": "two_redirects_https_via_http_initial",
                },
                {
                    "ip": "1.0.7.3",
                    "body": "Second step: HTTP",
                },
            ]
        },
        "two_redirects_http_via_https": {
            "ip": "1.0.8.1",
            "body": "two redirects: HTTP via HTTPS",
            "chain": [
                {
                    "ip": "1.0.8.2",
                    "body": "First step: HTTP",
                },
                {
                    "ip": "1.0.8.3",
                    "body": "Second step: HTTPS",
                    "tls": "two_redirects_https_via_http_middle",
                },
            ]
        },
        "two_redirects_no_https": {
            "ip": "1.0.9.1",
            "body": "two redirects: no HTTPS",
            "chain": [
                {
                    "ip": "1.0.9.2",
                    "body": "First step: HTTP",
                },
                {
                    "ip": "1.0.9.3",
                    "body": "Second step: HTTP",
                },
            ]
        },
    }

    PORTS = [80, 443]
    PROTOS = [protocols.HTTP, protocols.HTTPS]

    def setUp(self):
        from ztag.annotation import Annotation
        Annotation.load_annotations(False)
        self.zgrab_inputs = {
            case_id: get_zgrab_http_response(**kwargs) for case_id, kwargs in self.CASES.items()
        }
        self.expected_outputs = {
            case_id: get_expected_output(**kwargs) for case_id, kwargs in self.CASES.items()
        }

    def run_case(self, port, proto, case_id):
        """
        Do basically what the __main__ does, and check that the eventual encoding of the zgrab
        output matches the expected output.
        :param port:
        :param proto:
        :param case_id:
        :return:
        """
        from ztag.stream import Stream
        from ztag.transformer import ZMapTransformer
        from ztag.annotator import Annotator
        from ztag.encoders import JSONEncoder

        transform = ZMapTransformer.find_transform(port, proto, proto.GET, scan_id=0)
        encoder = JSONEncoder
        tagger = Annotator(port, proto, proto.GET)
        transforms = [
            transform,
            tagger,
            encoder(),
        ]
        input_from_zgrab = self.zgrab_inputs[case_id]
        expected = self.expected_outputs[case_id]
        outgoing = Accumulator()
        stream = Stream(incoming=[input_from_zgrab], outgoing=outgoing, logger=logger, transforms=transforms)
        stream.run()
        actual = [json.loads(o) for o in outgoing]
        self.assertEquals(len(actual), 1)
        self.assertEqual(json.dumps(expected, sort_keys=True, indent=2), json.dumps(actual[0], sort_keys=True, indent=2))

    def test_https_tls_handling(self):
        for proto in self.PROTOS:
            for case_id in self.CASES:
                for port in self.PORTS:
                    self.run_case(case_id=case_id, port=port, proto=proto)


if __name__ == '__main__':
    unittest.main()
