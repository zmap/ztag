from ztag.annotation import *

class SynologyDiskStationHTTPTitle(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        t = obj["title"].strip()

        if t.startswith("Synology DiskStation") or t.startswith("DiskStation2"):
            meta.global_metadata.manufacturer = Manufacturer.SYNOLOGY
            meta.global_metadata.product = "DiskStation"
            meta.global_metadata.device_type = Type.NAS
            meta.tags.add("embedded")
            return meta

        if t.endswith("DiskStation") and "Synology" in t:
            meta.global_metadata.manufacturer = Manufacturer.SYNOLOGY
            meta.global_metadata.product = "DiskStation"
            meta.global_metadata.device_type = Type.NAS
            meta.tags.add("embedded")
            return meta

        if t.endswith("RackStation") and "Synology" in t:
            meta.global_metadata.manufacturer = Manufacturer.SYNOLOGY
            meta.global_metadata.product = "RackStation"
            meta.global_metadata.device_type = Type.NAS
            meta.tags.add("embedded")
            return meta

        if "Synology Web Station" in t:
            meta.global_metadata.manufacturer = Manufacturer.SYNOLOGY
            meta.global_metadata.product = "WebStation"
            meta.global_metadata.device_type = Type.NAS
            meta.tags.add("embedded")
            return meta


class SynologyHTTPS(Annotation):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    tests = {
      "synology_https":{
        "global_metadata":{
          "manufacturer":Manufacturer.SYNOLOGY,
          "device_type":Type.NAS,
        },
        "tags":["embedded",]
      }
    }

    def process(self, obj, meta):
        cn = obj["certificate"]["parsed"]["issuer"]["common_name"][0]
        if cn == "Synology Inc. CA":
            meta.global_metadata.manufacturer = Manufacturer.SYNOLOGY
            meta.global_metadata.device_type = Type.NAS
            meta.tags.add("embedded")
            return meta
