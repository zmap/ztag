import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpAcp(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    manufact_re = re.compile("^220 AP\d+ Network Management Card AOS")
    product_re = re.compile("^220 (AP\d+)", re.IGNORECASE)

    def process(self, obj, meta):
        banner = obj["banner"]
        changed = False

        if self.manufact_re.search(banner):
            meta.global_metadata.device_type = Type.PDU
            meta.global_metadata.manufacturer = Manufacturer.APC
            product = self.product_re.search(banner).group(1)
            meta.global_metadata.product = product
            changed = True

        if changed:
            return meta
        else:
            return None

    """ Tests
    "220 AP9630 Network Management Card AOS v5.1.5 FTP server ready.\r\n"
    "220 AP9618 Network Management Card AOS v2.6.4 FTP server ready.\r\n"
    "220 AP9630 Network Management Card AOS v5.1.7 FTP server ready.\r\n"
    "220 AP8959 Network Management Card AOS v5.1.9 FTP server ready.\r\n"
    "220 AP7921 Network Management Card AOS v3.7.4 FTP server ready.\r\n"
    "220 AP7900 Network Management Card AOS v3.3.4 FTP server ready.\r\n"
    "220 AP7920 Network Management Card AOS v3.7.4 FTP server ready.\r\n"
    "220 AP7921 Network Management Card AOS v3.5.8 FTP server ready.\r\n"
    "220 AP7951 Network Management Card AOS v3.7.0 FTP server ready.\r\n"
    "220 AP7920 Network Management Card AOS v3.3.0 FTP server ready.\r\n"
    "220 AP9630 Network Management Card AOS v5.1.3 FTP server ready.\r\n"
    "220 AP9630 Network Management Card AOS v6.0.6 FTP server ready.\r\n"
    "220 AP7930 Network Management Card AOS v3.7.3 FTP server ready.\r\n"
    "220 AP7932 Network Management Card AOS v3.7.4 FTP server ready.\r\n"
    "220 AP8959 Network Management Card AOS v5.1.4 FTP server ready.\r\n"
    "220 AP7920 Network Management Card AOS v3.3.4 FTP server ready.\r\n"
    "220 AP8941 Network Management Card AOS v5.1.2 FTP server ready.\r\n"
    "220 AP7932 Network Management Card AOS v3.5.6 FTP server ready.\r\n"
    "220 AP7921 Network Management Card AOS v3.5.8 FTP server ready.\r\n"
    """
