from ztag.annotation import *


class RaritanHTTPS(TLSTag):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    def process(self, obj, meta):
        cn = obj["certificate"]["parsed"]["subject"]["common_name"][0]
        if cn == "Raritan Device":
            meta.global_metadata.manufacturer = Manufacturer.RARITAN
            meta.tags.add("embedded")
            meta.tags.add("data center")
            return meta


class RaritanHTTPLogo(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        if "logo_rar_tag_white.gif" in obj["body"]:
            meta.global_metadata.manufacturer = Manufacturer.RARITAN
            meta.tags.add("embedded")
            meta.tags.add("data center")
        if "Dominion" in obj["body"]:
            meta.global_metadata.device_type = Type.KVM
            meta.global_metadata.product = "Dominion"
        return meta
