import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpLexmark(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    manufact_re = re.compile(
        "^220( \w+)? Lexmark \w+ FTP Server",
        re.IGNORECASE
        )
    product_re = re.compile("^220 .+ Lexmark (.+) FTP Server", re.IGNORECASE)

    tests = {
        "FtpLexmark_1": {
            "global_metadata": {
                "device_type": Type.GENERIC_PRINTER,
                "manufacturer": Manufacturer.LEXMARK,
                "product": "E460dn"
            }
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.manufact_re.search(banner):
            meta.global_metadata.device_type = Type.GENERIC_PRINTER
            meta.global_metadata.manufacturer = Manufacturer.LEXMARK

            product = self.product_re.search(banner).group(1)
            meta.global_metadata.product = product

        return meta

    """ Tests
    "220 ET0021B7ECFD08 Lexmark X656de FTP Server NR.APS.N504 ready.\r\n"
    "220 ET0021B7E2BA2A Lexmark X543 FTP Server NR.APS.N469 ready.\r\n"
    "220 ET000400B3241B Lexmark T640 FTP Server NS.NP.N118 ready.\r\n"
    "220 ET000400F5CE61 Lexmark E342n FTP Server BR.H.P026 ready.\r\n"
    "220 LXKE25B68 Lexmark T520 FTP Server 54.20.22 ready.\r\n"
    "220 ET0021B772A0D1 Lexmark E460dn FTP Server NR.APS.N632 ready.\r\n"
    "220 ET0021B706CB8C Lexmark X658de FTP Server NR.APS.N644 ready.\r\n"
    "220 ET000400F392CD Lexmark T640 FTP Server NS.NP.N118 ready.\r\n"
    "220 ET0021B7C21663 Lexmark X792 FTP Server NH.HS40.N440 ready.\r\n"
    "220 ET000400156C71 Lexmark T640 FTP Server NS.NP.N118 ready.\r\n"
    "220 LXKEBA700 Lexmark T630 FTP Server 55.10.19 ready.\r\n"
    """
