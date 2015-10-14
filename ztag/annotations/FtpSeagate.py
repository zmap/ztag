import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpSeagate(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    manufact_1_re = re.compile(
        "^220 Welcome to Seagate Central Shared Storage FTP service",
        re.IGNORECASE
        )

    manufact_2_re = re.compile(
        "^220 Seagate-((DP[24])|(D[24])|(NAS)|(R4)) FTP Server \[",
        re.IGNORECASE
        )
    product_re = re.compile("Seagate-([-A-Za-z0-9_]+)", re.IGNORECASE)

    tests = {
        "FtpSeagate_1": {
            "global_metadata": {
                "device_type": Type.NAS,
                "manufacturer": Manufacturer.SEAGATE,
                "product": "Seagate Central"
            }
        },
        "FtpSeagate_2": {
            "global_metadata": {
                "device_type": Type.NAS,
                "manufacturer": Manufacturer.SEAGATE,
                "product": "DP4"
            }
        },
    }


    def process(self, obj, meta):
        banner = obj["banner"]

        if self.manufact_1_re.search(banner):
            meta.global_metadata.device_type = Type.NAS
            meta.global_metadata.manufacturer = Manufacturer.SEAGATE
            meta.global_metadata.product = "Seagate Central"

            return meta

        if self.manufact_2_re.search(banner):
            meta.global_metadata.device_type = Type.NAS
            meta.global_metadata.manufacturer = Manufacturer.SEAGATE
            product = self.product_re.search(banner).group(1)
            meta.global_metadata.product = product

            return meta

    """ Tests
    "220 Welcome to Seagate Central Shared Storage FTP service.\r\n"
    "220 Welcome to Seagate Central Shared Storage FTP service.\r\n"
    "220 Seagate-DP4 FTP Server [::ffff:192.168.1.50]\r\n"
    "220 Welcome to Seagate Central Shared Storage FTP service.\r\n"
    "220 Welcome to Seagate Central Shared Storage FTP service.\r\n"
    "220 Welcome to Seagate Central Shared Storage FTP service.\r\n"
    "220 Welcome to Seagate Central Shared Storage FTP service.\r\n"
    "220 Welcome to Seagate Central Shared Storage FTP service.\r\n"
    "220 Welcome to Seagate Central Shared Storage FTP service.\r\n"
    "220 Welcome to Seagate Central Shared Storage FTP service.\r\n"
    "220 Welcome to Seagate Central Shared Storage FTP service.\r\n"
    "220 Welcome to Seagate Central Shared Storage FTP service.\r\n"
    "220 Welcome to Seagate Central Shared Storage FTP service.\r\n"
    "220 Welcome to Seagate Central Shared Storage FTP service.\r\n"
    "220 Welcome to Seagate Central Shared Storage FTP service.\r\n"
    "220 Welcome to Seagate Central Shared Storage FTP service.\r\n"
    "220 Welcome to Seagate Central Shared Storage FTP service.\r\n"
    "220 Welcome to Seagate Central Shared Storage FTP service.\r\n"
    "220 Welcome to Seagate Central Shared Storage FTP service.\r\n"
    "220 Welcome to Seagate Central Shared Storage FTP service.\r\n"
    "220 Welcome to Seagate Central Shared Storage FTP service.\r\n"
    "220 Seagate-D2 FTP Server [::ffff:192.168.1.104]\r\n"
    """
