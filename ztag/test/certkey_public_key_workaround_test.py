from ztag.schema import ztag_ssh_v2
from zschema.compounds import *
from zschema.leaves import *


class CertkeyPublicKeyWorkaroundTestCase(unittest.TestCase):
    """
    Tests for workarounds added on 2018/09/07 (see schema.py).
    """
    def setUp(self):
        pass

    @staticmethod
    def get_bq(input):
        return {field['name']: field['type'] for field in input['fields']}
        
    def test_to_es(self):
        """
        Ensure that the to_es actually does exclude id, but that to_bq remains the same.
        """
        expected_es = {'properties': {'name': {'type': 'keyword'}}}
        expected_bq = {'id': 'INTEGER', 'name': 'STRING'}
        
        the_type = ztag_ssh_v2['server_host_key']['certkey_public_key']['type']
        actual_bq = self.get_bq(the_type.to_bigquery('type'))
        actual_es = the_type.to_es()
        self.assertDictEqual(expected_es, actual_es)
        self.assertDictEqual(expected_bq, actual_bq)

    def test_uint32_is_unmodified(self):
        """
        Ensure that other types with Unsigned32BitInteger fields are not affected.
        """
        other_type = SubRecord({
            'id': Unsigned32BitInteger(),
            'name': String(),
        })
        expected_es = {
            'properties': {
                'name': {'type': 'keyword'},
                'id': {'type': 'long'},
            }
        }
        expected_bq = {'id': 'INTEGER', 'name': 'STRING'}
        actual_bq = self.get_bq(other_type.to_bigquery("other_type"))
        actual_es = other_type.to_es()
        self.assertDictEqual(expected_es, actual_es)
        self.assertDictEqual(expected_bq, actual_bq)

    def test_transform(self):
        """
        Test that the transform strips the cert_type.id field
        """
        grab = {
            "data":{
                "xssh":{
                    "server_id": {
                        "raw": "SSH-2.0-OpenSSH_7.2p2 Ubuntu-4ubuntu2.4",
                        "version": "2.0",
                        "software": "OpenSSH_7.2p2",
                        "comment": "Ubuntu-4ubuntu2.4"
                    },
                    "server_key_exchange": {
                        "cookie": "dl2LAEeZ7cvx0xQrjs3PXw==",
                        "kex_algorithms": [
                            "curve25519-sha256@libssh.org",
                            "ecdh-sha2-nistp256",
                            "ecdh-sha2-nistp384",
                            "ecdh-sha2-nistp521",
                            "diffie-hellman-group-exchange-sha256",
                            "diffie-hellman-group14-sha1"
                        ],
                        "host_key_algorithms": [
                            "ssh-rsa",
                            "rsa-sha2-512",
                            "rsa-sha2-256",
                            "ecdsa-sha2-nistp256",
                            "ssh-ed25519"
                        ],
                        "client_to_server_ciphers": [
                            "chacha20-poly1305@openssh.com",
                            "aes128-ctr",
                            "aes192-ctr",
                            "aes256-ctr",
                            "aes128-gcm@openssh.com",
                            "aes256-gcm@openssh.com"
                        ],
                        "server_to_client_ciphers": [
                            "chacha20-poly1305@openssh.com",
                            "aes128-ctr",
                            "aes192-ctr",
                            "aes256-ctr",
                            "aes128-gcm@openssh.com",
                            "aes256-gcm@openssh.com"
                        ],
                        "client_to_server_macs": [
                            "umac-64-etm@openssh.com",
                            "umac-128-etm@openssh.com",
                            "hmac-sha2-256-etm@openssh.com",
                            "hmac-sha2-512-etm@openssh.com",
                            "hmac-sha1-etm@openssh.com",
                            "umac-64@openssh.com",
                            "umac-128@openssh.com",
                            "hmac-sha2-256",
                            "hmac-sha2-512",
                            "hmac-sha1"
                        ],
                        "server_to_client_macs": [
                            "umac-64-etm@openssh.com",
                            "umac-128-etm@openssh.com",
                            "hmac-sha2-256-etm@openssh.com",
                            "hmac-sha2-512-etm@openssh.com",
                            "hmac-sha1-etm@openssh.com",
                            "umac-64@openssh.com",
                            "umac-128@openssh.com",
                            "hmac-sha2-256",
                            "hmac-sha2-512",
                            "hmac-sha1"
                        ],
                        "client_to_server_compression": [
                            "none",
                            "zlib@openssh.com"
                        ],
                        "server_to_client_compression": [
                            "none",
                            "zlib@openssh.com"
                        ],
                        "first_kex_follows": False,
                        "reserved": 0
                    },
                    "algorithm_selection": {
                        "dh_kex_algorithm": "curve25519-sha256@libssh.org",
                        "host_key_algorithm": "ecdsa-sha2-nistp256",
                        "client_to_server_alg_group": {
                            "cipher": "aes128-ctr",
                            "mac": "hmac-sha2-256",
                            "compression": "none"
                        },
                        "server_to_client_alg_group": {
                            "cipher": "aes128-ctr",
                            "mac": "hmac-sha2-256",
                            "compression": "none"
                        }
                    },
                    "key_exchange": {
                        "curve25519_sha256_params": {
                            "server_public": "d4LbboNPD+8feM4s2PjROJW07xbSpBq/rQSldP8SnAI="
                        },
                        "server_signature": {
                            "parsed": {
                                "algorithm": "ecdsa-sha2-nistp256",
                                "value": "AAAAIFqqEqz8qdIqvCHDUQzepCw/fRpyQFHaHjkLvg9C+NJ7AAAAIFRVK"
                                         "DWwRPnaRlrvL3147jTgAf4qAehT4D3Q/RW/LvlX"
                            },
                            "raw": "AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAABIAAAAIFqqEqz8qdIqvCHDUQzepCw"
                                   "/fRpyQFHaHjkLvg9C+NJ7AAAAIFRVKDWwRPnaRlrvL3147jTgAf4qAehT4D3Q/R"
                                   "W/LvlX",
                            "h": "haFWxro3i4labGImawWJNSwaYHLTXHuGPkftgpn2/Fw="
                        },
                        "server_host_key": {
                            "certkey_public_key": {
                                "cert_type": {
                                    "name": "UNKNOWN",
                                    "id": 123,
                                }
                            },
                            "algorithm": "ecdsa-sha2-nistp256",
                            "fingerprint_sha256": "691e8c65d86720d072fc5610f8976df184af64a91aea986a"
                                                  "2de55a1abc0179dc"
                        }
                    }
                }
            }
        }
        from ztag.transforms import SSHV2Transform
        expected = {
            "name": "UNKNOWN"
        }
        xform = SSHV2Transform(port=SSHV2Transform.port,
                               protocol=SSHV2Transform.protocol,
                               subprotocol=SSHV2Transform.subprotocol,
                               scan_id='fake')
        transformed = xform._transform_object(grab)
        actual = transformed.transformed['server_host_key']['certkey_public_key']['type']
        self.assertEquals(expected, actual)



