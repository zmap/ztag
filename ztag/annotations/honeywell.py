from ztag.annotation import *

class HoneywellNotifier(TLSTag):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    tests = {
      "honeywell_notifier":{
        "global_metadata":{
          "manufacturer":Manufacturer.HONEYWELL,
          "device_type":Type.FIRE_ALARM,
          "product":"Notifier",
        },
        "tags":["embedded", "building control"]
      }
    }

    def process(self, obj,meta):
        o = obj["certificate"]["parsed"]["issuer"]["organization"][0]
        ou = obj["certificate"]["parsed"]["issuer"]["organizational_unit"][0]
        if o == "Honeywell" and ou == "Notifier":
            meta.global_metadata.manufacturer = Manufacturer.HONEYWELL
            meta.global_metadata.product = "Notifier"
            meta.global_metadata.device_type = Type.FIRE_ALARM
            meta.tags.add("building control")
            meta.tags.add("embedded")
            return meta


