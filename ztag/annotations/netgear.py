from ztag.annotation import *

class NetGearSmartSwitch(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    tests = {
      "netgear_smart_switch":{
        "global_metadata":{
          "manufacturer":Manufacturer.NETGEAR,
          "device_type":Type.SWITCH,
          "product":"Smart Switch",
        },
        "tags":["embedded",]
      }
    }

    def process(self, obj, meta):
        if obj["title"] == "NETGEAR Web Smart Switch":
            meta.global_metadata.manufacturer = Manufacturer.NETGEAR
            meta.global_metadata.product = "Smart Switch"
            meta.global_metadata.device_type = Type.SWITCH
            meta.tags.add("embedded")
            return meta
        if obj["title"] == "Netgear Prosafe Plus Switch":
            meta.global_metadata.manufacturer = Manufacturer.NETGEAR
            meta.global_metadata.product = "Prosafe Plus Switch"
            meta.global_metadata.device_type = Type.SWITCH
            meta.tags.add("embedded")
            return meta


class NetGearLabeledSwitches(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    VALID_MODELS = set([
        "GS724T",
        "GS748Tv5",
        "GS108T"
    ])

    def process(self, obj, meta):
        if obj["title"].lower().startswith("netgear") and " " in obj["title"]:
            m = obj["title"].split(" ")[1].strip()
            if m in self.VALID_MODELS:
                meta.global_metadata.manufacturer = Manufacturer.NETGEAR
                meta.global_metadata.product = m
                meta.global_metadata.device_type = Type.SWITCH
                meta.tags.add("embedded")
                return meta


class NetGearProsafe(Annotation):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    tests = {
      "netgear_prosafe":{
        "global_metadata":{
          "manufacturer":Manufacturer.NETGEAR,
          "device_type":Type.FIREWALL,
          "product":"Prosafe VPN Firewall",
        },
        "tags":["embedded",]
      }
    }

    def process(self, obj, meta):
        cn = obj["certificate"]["parsed"]["subject"]["common_name"][0].strip()
        if cn == "Netgear VPN Firewall":
            meta.global_metadata.manufacturer = Manufacturer.NETGEAR
            meta.global_metadata.product = "Prosafe VPN Firewall"
            meta.global_metadata.device_type = Type.FIREWALL
            meta.tags.add("embedded")
            return meta

