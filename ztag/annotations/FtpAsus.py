import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpAsus(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    manufact_1_re = re.compile("^220 Welcome to ASUS", re.IGNORECASE)
    product_1_re = re.compile(
                        "220 Welcome to ASUS (.+) FTP service",
                        re.IGNORECASE
                        )

    manufact_2_re = re.compile(
        "^220 Welcome to the WL700gE FTP service",
        re.IGNORECASE
        )

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.manufact_1_re.search(banner):
            meta.global_metadata.device_type = Type.SOHO_ROUTER
            meta.global_metadata.manufacturer = Manufacturer.ASUS

            product = self.product_1_re.search(banner).group(1)
            meta.global_metadata.product = product

        if self.manufact_2_re.search(banner):
            meta.global_metadata.device_type = Type.SOHO_ROUTER
            meta.global_metadata.manufacturer = Manufacturer.ASUS
            meta.global_metadata.product = "WL700gE"

        return meta

    """ Tests
    "220 Welcome to the WL700gE FTP service.\r\n"
    "220 Welcome to the WL700gE FTP service.\r\n"
    "220 Welcome to the WL700gE FTP service.\r\n"
    "220 Welcome to the WL700gE FTP service.\r\n"
    "220 Welcome to the WL700gE FTP service.\r\n"
    "220 Welcome to the WL700gE FTP service.\r\n"
    "220 Welcome to the WL700gE FTP service.\r\n"
    "220 Welcome to ASUS RT-AC66U FTP service.\r\n"
    "220 Welcome to ASUS RT-AC66U FTP service.\r\n"
    "220 Welcome to ASUS RT-N56U FTP service.\r\n"
    "220 Welcome to ASUS RT-AC68U FTP service.\r\n"
    "220 Welcome to ASUS RT-N66W FTP service.\r\n"
    "220 Welcome to ASUS RT-N10U FTP service.\r\n"
    "220 Welcome to ASUS RT-N66R FTP service.\r\n"
    "220 Welcome to ASUS RT-N18U FTP service.\r\n"
    "220 Welcome to ASUS RT-AC68U FTP service.\r\n"
    "220 Welcome to ASUS RT-AC68U FTP service.\r\n"
    "220 Welcome to ASUS RT-N66U FTP service.\r\n"
    "220 Welcome to ASUS RT-AC66U FTP service.\r\n"
    "220 Welcome to ASUS RT-N65U FTP service.\r\n"
    "220 Welcome to ASUS DSL-N55U FTP service.\r\n"
    "220 Welcome to ASUS RT-AC68U FTP service.\r\n"
    "220 Welcome to ASUS RT-AC51U FTP service.\r\n"
    "220 Welcome to ASUS RT-N16 FTP service.\r\n"
    "220 Welcome to ASUS DSL-AC68U FTP service.\r\n"
    "220 Welcome to ASUS RT-N65U FTP service.\r\n"
    "220 Welcome to ASUS RT-AC66U FTP service.\r\n"
    "220 Welcome to ASUS RT-AC66U FTP service.\r\n"
    "220 Welcome to ASUS RT-N65U FTP service.\r\n"
    "220 Welcome to ASUS RT-AC68W FTP service.\r\n"
    "220 Welcome to ASUS RT-AC56U FTP service.\r\n"
    "220 Welcome to ASUS RT-AC66U FTP service.\r\n"
    "220 Welcome to ASUS RT-AC55U FTP service.\r\n"
    "220 Welcome to ASUS RT-AC56U FTP service.\r\n"
    "220 Welcome to ASUS RT-AC56U FTP service.\r\n"
    "220 Welcome to ASUS DSL-N55U FTP service.\r\n"
    "220 Welcome to ASUS RT-N66U FTP service.\r\n"
    """
