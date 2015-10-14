import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpWesternDigital(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    productDict = {
        "MyCloud": re.compile("^220 Welcome to WD My Cloud", re.IGNORECASE),
        "MyBookLive": re.compile(
            "^220 \"Welcome to MyBookLive",
            re.IGNORECASE
            )
    }

    tests = {
        "FtpWesternDigital_1": {
            "global_metadata": {
                "device_type": Type.NAS,
                "manufacturer": Manufacturer.WESTERN_DIGITAL,
                "product": "MyBookLive",
            }
        },
        "FtpWesternDigital_2": {
            "global_metadata": {
                "device_type": Type.NAS,
                "manufacturer": Manufacturer.WESTERN_DIGITAL,
                "product": "MyCloud",
            }
        },
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        for product, regex in self.productDict.items():
            if regex.search(banner):
                meta.global_metadata.device_type = Type.NAS
                meta.global_metadata.product = product

                temp = Manufacturer.WESTERN_DIGITAL
                meta.global_metadata.manufacturer = temp

                return meta

    """ Tests
    "220 \"Welcome to MyBookLive\"\r\n"
    "220 Welcome to WD My Cloud\r\n"
    "220 Welcome to WD My Cloud\r\n"
    "220 \"Welcome to MyBookLive\"\r\n"
    "220 \"Welcome to MyBookLive\"\r\n"
    "220 \"Welcome to MyBookLive\"\r\n"
    "220 Welcome to WD My Cloud\r\n"
    "220 Welcome to WD My Cloud\r\n"
    "220 Welcome to WD My Cloud\r\n"
    "220 Welcome to WD My Cloud\r\n"
    "220 \"Welcome to MyBookLive\"\r\n"
    "220 Welcome to WD My Cloud\r\n"
    "220 \"Welcome to MyBookLive\"\r\n"
    """
