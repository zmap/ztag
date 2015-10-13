from ztag.annotation import Annotation
from ztag import protocols
import ztag.test


class KonicaMinolta(Annotation):
    name = "KonicaMinolta"
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    def process(self, obj, meta):
        banner = obj["banner"]

        if banner.startswith("220 KONICA MINOLTA FTP server ready"):
            meta.global_metadata.manufacturer = Manufacturer.KONICA_MINOLTA
            meta.global_metadata.device_type = Type.GENERIC_PRINTER

        return meta
