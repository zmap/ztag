import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpSony(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    manufact_1_re = re.compile(
        "^220 Welcome to SONY Network Camera",
        re.IGNORECASE
        )

    manufact_2_re = re.compile("^220-Sony Network Camera", re.IGNORECASE)
    product_2_re = re.compile("Network Camera ([-A-Z0-9_]+)", re.IGNORECASE)

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.manufact_1_re.search(banner):
            meta.global_metadata.device_type = Type.CAMERA
            meta.global_metadata.manufacturer = Manufacturer.SONY

        if self.manufact_2_re.search(banner):
            meta.global_metadata.device_type = Type.CAMERA
            meta.global_metadata.manufacturer = Manufacturer.SONY
            product = self.product_2_re.search(banner).group(1)
            meta.global_metadata.product = product

        return meta

    """ Tests
    "220-Sony Network Camera SNC-EP520\r\n220 \r\n"
    "220 Welcome to SONY Network Camera\r\n"
    "220-Sony Network Camera SNC-CH140\r\n220 \r\n"
    "220 Welcome to SONY Network Camera\r\n"
    "220 Welcome to SONY Network Camera\r\n"
    "220-Sony Network Camera SNC-ER580\r\n220 \r\n"
    "220-Sony Network Camera SNC-DH160\r\n220 \r\n"
    """
