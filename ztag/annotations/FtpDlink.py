import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpDlink(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    manufact_1_re = re.compile(
                        "^220 Welcome to DCS-\d+[A-Z+]? FTP Server",
                        re.IGNORECASE
                        )
    product_1_re = re.compile(
                        "^220 Welcome to (DCS-\d+[+A-Z]?) FTP",
                        re.IGNORECASE
                        )
    manufact_2_re = re.compile(
                        "^220 DCS-\d+[A-Z+]? FTP server ready",
                        re.IGNORECASE
                        )
    product_2_re = re.compile("^220 (DCS-\d+[+A-Z]?) FTP", re.IGNORECASE)

    tests = {
        "FtpDlink_1": {
            "global_metadata": {
                "device_type": Type.CAMERA,
                "manufacturer": Manufacturer.DLINK,
                "product": "DCS-2100+"
            }
        },
        "FtpDlink_2": {
            "global_metadata": {
                "device_type": Type.CAMERA,
                "manufacturer": Manufacturer.DLINK,
                "product": "DCS-6620G"
            }
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.manufact_1_re.search(banner):
            meta.global_metadata.device_type = Type.CAMERA
            meta.global_metadata.manufacturer = Manufacturer.DLINK
            product = self.product_1_re.search(banner).group(1)
            meta.global_metadata.product = product
            return meta

        if self.manufact_2_re.search(banner):
            meta.global_metadata.device_type = Type.CAMERA
            meta.global_metadata.manufacturer = Manufacturer.DLINK
            product = self.product_2_re.search(banner).group(1)
            meta.global_metadata.product = product
            return meta


    """ Tests
    "220 DCS-5300 FTP server ready.\r\n"
    "220 DCS-2100G FTP server ready.\r\n"
    "220 Welcome to DCS-6620G FTP Server\r\n"
    "220 DCS-5300 FTP server ready.\r\n"
    "220 DCS-5300G FTP server ready.\r\n"
    "220 Welcome to DCS-6620G FTP Server\r\n"
    "220 DCS-5300 FTP server ready.\r\n"
    "220 DCS-2100+ FTP server ready.\r\n"
    "220 Welcome to DCS-3420 FTP Server\r\n"
    "220 DCS-2100+ FTP server ready.\r\n"
    "220 DCS-5300G FTP server ready.\r\n"
    "220 Welcome to DCS-6620G FTP Server\r\n"
    "220 Welcome to DCS-6620G FTP Server\r\n"
    "220 DCS-5300 FTP server ready.\r\n"
    "220 DCS-5300 FTP server ready.\r\n"

    """
