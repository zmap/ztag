import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag import protocols
import ztag.test


class FtpXlight(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    product_re = re.compile(
        "^220 Xlight FTP(?: Server)? \d+\.\d+",
        re.IGNORECASE
        )
    version_re = re.compile("FTP(?: Server)? (\d+\.\d+)", re.IGNORECASE)

    tests = {
        "FtpXlight_1": {
            "global_metadata": {
                "os": OperatingSystem.WINDOWS,
            },
            "local_metadata": {
                "product": "Xlight",
                "version": "3.8"
            }
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.product_re.search(banner):
            meta.global_metadata.os = OperatingSystem.WINDOWS

            meta.local_metadata.product = "Xlight"

            version = self.version_re.search(banner).group(1)
            meta.local_metadata.version = version

            return meta

    """ Tests
    "220 Xlight FTP Server 2.4 ready...\r\n"
    "220 Xlight FTP Server 3.7 ready...\r\n"
    "220 Xlight FTP Server 3.8 ready...\r\n"
    "220 Xlight FTP Server 3.8 ready...\r\n"
    "220 Xlight FTP 3.6.5 \\xbe\\xcd\\xd0\\xf7...\r\n"
    "220 Xlight FTP 3.6 \\xbe\\xcd\\xd0\\xf7...\r\n"
    "220 Xlight FTP 3.7 \\xbe\\xcd\\xd0\\xf7...\r\n"
    "220 Xlight FTP 3.7 \\xbe\\xcd\\xd0\\xf7...\r\n"
    "220 Xlight FTP Server 3.7 ready...\r\n"
    "220 Xlight FTP 3.7 \\xbe\\xcd\\xd0\\xf7...\r\n"
    "220 Xlight FTP 3.6 \\xbe\\xcd\\xd0\\xf7...\r\n"
    "220 Xlight FTP Server 3.5 ready...\r\n"
    """
