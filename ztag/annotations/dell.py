from ztag.annotation import *

class DellCMC(TLSTag):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    tests = {
      "dell_chassis_management_controller":{
        "global_metadata":{
          "manufacturer":Manufacturer.DELL,
          "device_type":Type.SERVER_MANAGEMENT,
          "product":"Chassis Management Controller",
        },
        "tags":["embedded", "data center"]
      }
    }

    def process(self, obj,meta):
        ou = obj["certificate"]["parsed"]["issuer"]["organizational_unit"][0]
        if ou == "OpenCMC Group":
            meta.global_metadata.manufacturer = Manufacturer.DELL
            meta.global_metadata.device_type = Type.SERVER_MANAGEMENT
            meta.global_metadata.product = "Chassis Meanagement Controller"
            meta.tags.add("embedded")
            meta.tags.add("data center")
            return meta

class DellIDRAC(TLSTag):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    tests = {
      "dell_idrac":{
        "global_metadata":{
          "manufacturer":Manufacturer.DELL,
          "device_type":Type.SERVER_MANAGEMENT,
          "product":"Integrated Dell Remote Access Controller",
        },
        "tags":["embedded", "data center"]
      }
    }

    def process(self, obj,meta):
        o = obj["certificate"]["parsed"]["issuer"]["organization"][0]
        ou = obj["certificate"]["parsed"]["issuer"]["organizational_unit"][0]
        if o == "Dell Inc." and ou == "Remote Access Group":
            meta.global_metadata.manufacturer = Manufacturer.DELL
            meta.global_metadata.product = "Integrated Dell Remote Access Controller"
            meta.global_metadata.device_type = Type.SERVER_MANAGEMENT
            meta.tags.add("embedded")
            meta.tags.add("data center")
            return meta


