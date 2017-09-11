from ztag.annotation import *


class CiscoServer(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    tests = {
        "cisco_server":{
            "global_metadata":{
                "manufacturer":"Cisco",
            }
        }
    }

    def process(self, obj, meta):
        server = obj["headers"]["server"]
        if "cisco" in server.lower():
            meta.global_metadata.manufacturer = "Cisco"
            return meta


class CiscoUnifiedIPPhone(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        if obj["title"] == "Cisco Systems, Inc.":
            meta.global_metadata.manufacturer = Manufacturer.CISCO
            meta.tags.add("embedded")
            if "IP Phone" in obj["body"]:
                meta.global_metadata.product = "IP Phone"
                meta.global_metadata.device_type = Type.PHONE
                if "CP-7945G" in obj["body"]:
                    meta.global_metadata.product = "IP Phone CP-7945G"
                if "CP-7942G" in obj["body"]:
                    meta.global_metadata.product = "IP PHone CP-7945G"
                if "CP-7960G" in obj["body"]:
                    meta.global_metadata.product = "IP PHone CP-7960G"
            return meta


class CiscoGenericSwitch(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        if obj["title"] == "Switch":
            if "cisco_logo_header" in obj["body"]:
                meta.global_metadata.device_type = Type.SWITCH
                meta.global_metadata.manufacturer = Manufacturer.CISCO
                meta.tags.add("embedded")
                return meta


class CiscoTempASACertificate(TLSTag):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    def process(self, obj,meta):
        cn = obj["certificate"]["parsed"]["subject"]["common_name"][0]
        if cn == "ASA Temporary Self Signed Certificate":
            meta.global_metadata.manufacturer = Manufacturer.CISCO
            meta.global_metadata.device_type = Type.NETWORK
            meta.tags.add("embedded")
            return meta


class CiscoRV082(TLSTag):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    def process(self, obj,meta):
        o = obj["certificate"]["parsed"]["subject"]["organization"][0]
        ou = obj["certificate"]["parsed"]["subject"]["organizational_unit"][0]
        if o == "Cisco Systems, Inc." and ou == "RV082":
            meta.global_metadata.manufacturer = Manufacturer.CISCO
            meta.global_metadata.device_type = Type.SOHO_ROUTER
            meta.global_metadata.product = "RV082 Dual WAN VPN Router"
            meta.tags.add("embedded")
            return meta

