import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpRouterBoard(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    manufact_1_re = re.compile(
        "^220 \d+ -> SXT.+ \(MikroTik \d+\.\d+(\.\d+)?\) ready",
        re.IGNORECASE
        )

    manufact_2_re = re.compile(
        "^220 \d+ -> \d+[A-Z]?((-5Hn(D)?)|(-5Hn-MMCX))? FTP server \(MikroTik \d+\.\d+(\.\d+)?\) ready",
        re.IGNORECASE
        )

    product_re = re.compile("^220 \d+ -> (.+) FTP server", re.IGNORECASE)

    implementation_re = re.compile(
        "^220 .+ FTP server \(MikroTik (\d+(?:\.\d+)*)\)",
        re.IGNORECASE
        )

    tests = {
        "FtpRouterBoard_1": {
            "global_metadata": {
                "manufacturer": Manufacturer.ROUTER_BOARD,
                "product": "711-5HnD"
            },
            "local_metadata": {
                "product": "MikroTik",
                "version": "6.10"
            }
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if (
            self.manufact_1_re.search(banner) or
            self.manufact_2_re.search(banner)
        ):

            meta.global_metadata.manufacturer = Manufacturer.ROUTER_BOARD

            product = self.product_re.search(banner).group(1)
            meta.global_metadata.product = product

            meta.local_metadata.product = "MikroTik"

            implementation = self.implementation_re.search(banner)
            meta.local_metadata.version = implementation.group(1)

        return meta

    """ Tests
    "220 002279 -> SXT 5nD r2 FTP server (MikroTik 6.23) ready\r\n"
    "220 003252 -> SXT 5nD r2 FTP server (MikroTik 6.20) ready\r\n"
    "220 003142 -> 711-5Hn-MMCX FTP server (MikroTik 6.26) ready\r\n"
    "220 004259 -> SXT 5HnD FTP server (MikroTik 6.12) ready\r\n"
    "220 004602 -> SXT 5HPnD FTP server (MikroTik 6.20) ready\r\n"
    "220 002853 -> 411 FTP server (MikroTik 6.26) ready\r\n"
    "220 002619 -> 411 FTP server (MikroTik 6.26) ready\r\n"
    "220 003940 -> 711-5HnD FTP server (MikroTik 6.10) ready\r\n"
    "220 005337 -> SXT 5nD r2 FTP server (MikroTik 6.13) ready\r\n"
    "220 001840 -> SXT 5nD r2 FTP server (MikroTik 6.13) ready\r\n"
    "220 003952 -> SXT 5HnD FTP server (MikroTik 6.29.1) ready\r\n"
    "220 004063 -> SXT 5HnD FTP server (MikroTik 6.19) ready\r\n"
    "220 005911 -> SXT 5nD r2 FTP server (MikroTik 6.13) ready\r\n"
    "220 006515 -> SXT 5nD r2 FTP server (MikroTik 6.19) ready\r\n"
    "220 005436 -> SXT 5nD r2 FTP server (MikroTik 6.13) ready\r\n"
    "220 000557 -> SXT 5HPnD FTP server (MikroTik 6.12) ready\r\n"
    "220 000771 -> SXT 5HnD FTP server (MikroTik 6.12) ready\r\n"
    "220 002549 -> 411 FTP server (MikroTik 6.27) ready\r\n"
    """
