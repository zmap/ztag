import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpFritz(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None
    manufact_re = re.compile("^220 FRITZ!Box", re.IGNORECASE)
    product_re = re.compile("^220 (.+) FTP server ready", re.IGNORECASE)

    tests = {
        "FtpFritz_1": {
            "global_metadata": {
                "device_type": Type.CABLE_MODEM,
                "manufacturer": Manufacturer.AVM,
                "product": "FRITZ!BoxFonWLAN7390"
            }
        },
        "FtpFritz_2": {
            "global_metadata": {
                "device_type": Type.CABLE_MODEM,
                "manufacturer": Manufacturer.AVM,
                "product": "FRITZ!BoxFonWLAN7360(EWEEdition)"
            }
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.manufact_re.search(banner):
            meta.global_metadata.device_type = Type.CABLE_MODEM
            meta.global_metadata.manufacturer = Manufacturer.AVM

            product = self.product_re.search(banner).group(1)
            meta.global_metadata.product = product

            return meta

    """ Tests
    "220 FRITZ!Box7272 FTP server ready.\r\n"
    "220 FRITZ!BoxFonWLAN7390 FTP server ready.\r\n"
    "220 FRITZ!Box7490 FTP server ready.\r\n"
    "220 FRITZ!BoxFonWLAN7390 FTP server ready.\r\n"
    "220 FRITZ!BoxFonWLAN7390 FTP server ready.\r\n"
    "220 FRITZ!BoxFonWLAN7170 FTP server ready.\r\n"
    "220 FRITZ!BoxFonWLAN7390(UI) FTP server ready.\r\n"
    "220 FRITZ!BoxFonWLAN7270v2 FTP server ready.\r\n"
    "220 FRITZ!BoxFonWLAN7390(UI) FTP server ready.\r\n"
    "220 FRITZ!BoxFonWLAN7360(EWEEdition) FTP server ready.\r\n"
    "220 FRITZ!Box7330SL(UI) FTP server ready.\r\n"
    "220 FRITZ!Box7490 FTP server ready.\r\n"
    "220 FRITZ!BoxFonWLAN7270v3 FTP server ready.\r\n"
    "220 FRITZ!BoxFonWLAN7340 FTP server ready.\r\n"
    "220 FRITZ!Box6360Cable(kdg) FTP server ready.\r\n"
    "220 FRITZ!Box6360Cable(um) FTP server ready.\r\n"
    """
