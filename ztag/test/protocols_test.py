from zsearch_definitions.protocols import Protocol, Subprotocol
import zsearch_definitions.protocols

import unittest


class ProtocolNameTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_from_name(self):
        protocol_long = "PROTO_HTTPS"
        protocol_short = "https"
        from_long = Protocol.from_name(protocol_long)
        from_short = Protocol.from_pretty_name(protocol_short)
        self.assertEqual(from_long.value, from_short.value)
        self.assertEqual(from_long.value, zsearch_definitions.protocols.HTTPS.value)

    def test_subprotocols_with_bonus_underscores(self):
        modbus = Protocol.from_pretty_name("modbus")
        self.assertTrue(hasattr(modbus, "DEVICE_ID"))
        self.assertFalse(hasattr(modbus, "MEI"))
        self.assertFalse(hasattr(modbus, "DEVICE"))

    def test_generic_subprotocols_exposed_as_attributes(self):
        proto_http = Protocol.from_pretty_name("http")
        self.assertTrue(hasattr(proto_http, "GET"))

if __name__ == '__main__':
    unittest.main()
