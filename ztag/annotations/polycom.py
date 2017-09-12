from ztag.annotation import *


class PolyComHTTPS(Annotation):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    def process(self, obj, meta):
        org = d["certificate"]["parsed"]["issuer"]["organization"][0]
        if org == "Polycom, Inc.":
            meta.global_metadata.manufacturer = "Polycom, Inc."
            meta.global_metadata.device_type = Type.CAMERA
            meta.tags.add("embedded")
            return meta


class PolycomHTTPTitle(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        if obj["title"] == "'+sysName+' - Polycom '+GetCurrentPageName ()+'":
            meta.global_metadata.manufacturer = Manufacturer.POLYCOM
            meta.global_metadata.device_type = Type.CAMERA
            meta.tags.add("embedded")
            return meta


class PolycomConfigurationHTTPTitle(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        if obj["title"] == "Polycom - Configuration Utility":
            meta.global_metadata.manufacturer = Manufacturer.POLYCOM
            meta.global_metadata.device_type = Type.CAMERA
            meta.tags.add("embedded")
            return meta

