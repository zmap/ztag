import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpXerox(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    manufact_1_re = re.compile(
        "^220 FUJI XEROX Docu((Print)|(Centre))",
        re.IGNORECASE
        )
    product_1_re = re.compile(
        "^220 FUJI XEROX (.+)",
        re.IGNORECASE
        )

    manufact_2_re = re.compile(
        "^220 Xerox Phaser",
        re.IGNORECASE
        )
    product_2_re = re.compile(
        "^220 Xerox (.+)",
        re.IGNORECASE
        )

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.manufact_1_re.search(banner):
            meta.global_metadata.device_type = Type.GENERIC_PRINTER
            meta.global_metadata.manufacturer = Manufacturer.XEROX
            product = product_1_re.search(banner).group(1)
            meta.global_metadata.product = product

        if self.manufact_2_re.search(banner):
            meta.global_metadata.device_type = Type.GENERIC_PRINTER
            meta.global_metadata.manufacturer = Manufacturer.XEROX
            product = product_2_re.search(banner).group(1)
            meta.global_metadata.product = product

        return meta

    """ Tests
    "220 Xerox Phaser 6500DN\r\n"
    "220 Xerox Phaser 6180MFP-D\r\n"
    "220 Xerox Phaser 6500DN\r\n"
    "220 FUJI XEROX DocuPrint M355 df\r\n"
    "220 Xerox Phaser 6125N\r\n"
    "220 Xerox Phaser 6280DN\r\n"
    "220 Xerox Phaser 6600N\r\n"
    "220 FUJI XEROX DocuPrint CP305 d\r\n"
    "220 Xerox Phaser 6600DN\r\n"
    "220 FUJI XEROX DocuPrint CM305 df\r\n"
    "220 FUJI XEROX DocuPrint 3055\r\n"
    "220 Xerox Phaser 3610\r\n"
    "220 FUJI XEROX DocuPrint M355 df\r\n"
    "220 FUJI XEROX DocuPrint 2065\r\n"
    "220 FUJI XEROX DocuPrint CP305 d\r\n"
    "220 Xerox Phaser 6280N\r\n"
    """
