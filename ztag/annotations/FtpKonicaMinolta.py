from ztag.annotation import Annotation
from ztag.annotation import Manufacturer
from ztag.annotation import Type
from ztag import protocols
import ztag.test


class FtpKonicaMinolta(Annotation):
    name = "KonicaMinolta"
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    tests = {
        "FtpKonicaMinolta_1": {
            "global_metadata": {
                "manufacturer": Manufacturer.KONICA_MINOLTA,
                "device_type": Type.GENERIC_PRINTER
            }
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if banner.startswith("220 KONICA MINOLTA FTP server ready"):
            meta.global_metadata.manufacturer = Manufacturer.KONICA_MINOLTA
            meta.global_metadata.device_type = Type.GENERIC_PRINTER

            return meta
