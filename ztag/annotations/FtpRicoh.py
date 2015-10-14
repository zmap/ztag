import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpRicoh(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    product_re = re.compile(
        "^220 RICOH (.+) FTP server \(\d+(?:\.\d+)*\) ready",
        re.IGNORECASE
        )

    version_re = re.compile(
        "FTP server \((\d+\.\d+)\) ready",
        re.IGNORECASE
        )

    tests = {
        "FtpRicoh_1": {
            "global_metadata": {
                "device_type": Type.GENERIC_PRINTER,
                "manufacturer": Manufacturer.RICOH,
                "product": "Aficio MP C2551"
            },
            "local_metadata": {
                "version": "10.56"
            }
        },
        "FtpRicoh_2": {
            "global_metadata": {
                "device_type": Type.GENERIC_PRINTER,
                "manufacturer": Manufacturer.RICOH,
                "product": "MP C2003"
            },
            "local_metadata": {
                "version": "12.78"
            }
        }
    }
                
    def process(self, obj, meta):
        banner = obj["banner"]

        if self.product_re.search(banner):
            meta.global_metadata.device_type = Type.GENERIC_PRINTER
            meta.global_metadata.manufacturer = Manufacturer.RICOH

            product = self.product_re.search(banner).group(1)
            meta.global_metadata.product = product

            version = self.version_re.search(banner).group(1)
            meta.local_metadata.version = version

            return meta

    """ Tests
    "220 RICOH Aficio MP C2551 FTP server (10.56) ready.\r\n"
    "220 RICOH Aficio SP C431DN FTP server (9.60) ready.\r\n"
    "220 RICOH Aficio MP 6002 FTP server (11.96.5) ready.\r\n"
    "220 RICOH Aficio MP C4502 FTP server (11.102) ready.\r\n"
    "220 RICOH MP C2003 FTP server (12.78) ready.\r\n"
    "220 RICOH MP C4503 FTP server (12.66) ready.\r\n"
    "220 RICOH Aficio MP 3351 FTP server (7.29.3) ready.\r\n"
    "220 RICOH Aficio MP C4502 FTP server (11.100) ready.\r\n"
    "220 RICOH Aficio MP 6002 FTP server (11.96.5) ready.\r\n"
    """
