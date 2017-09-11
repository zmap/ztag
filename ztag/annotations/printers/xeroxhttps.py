from ztag.annotation import Annotation, TLSTag

from ztag import protocols
import ztag.test


class XeroxHTTPS(TLSTag):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    def process(self, obj, meta):
        organization = obj["certificate"]["parsed"]["issuer"]["organization"]
        if "Xerox Corporation" == organization[0]:
            meta.global_metadata.manufacturer = Manufacturer.XEROX
            meta.tags.add("embedded")
        return meta


class XeroxWorkCenterHTTP(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        if obj["title"].startswith("XEROX WORKCENTRE"):
            meta.global_metadata.manufacturer = Manufacturer.XEROX
            meta.global_metadata.device_type = Type.PRINTER
            meta.global_metadata.product = "WorkCentre"
            meta.tags.add("embedded")
            return meta


class XeroxHTTP(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        if 'src="x_logo.gif" alt="Xerox"' in obj["body"]:
            meta.global_metadata.manufacturer = Manufacturer.XEROX
            meta.tags.add("embedded")
        if "Printer with Embedded Web Server" in obj["body"]:
            meta.global_metadata.device_type = Type.PRINTER
            meta.tags.add("embedded")
        return meta



class XeroxPhaser(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        t = obj["title"]
        if t.startswith("Xerox&nbsp;Phaser"):
            t = t[11:]
        if t.startswith("Phaser"):
            if "-" in t:
                t = t.strip().split("-")[0].strip()
            meta.global_metadata.manufacturer = Manufacturer.XEROX
            meta.global_metadata.device_type = Type.PRINTER
            meta.global_metadata.product = t
            meta.tags.add("embedded")
            return meta


