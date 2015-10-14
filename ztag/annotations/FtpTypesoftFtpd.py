import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag import protocols
import ztag.test


class FtpTypesoftFtpd(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    impl_re = re.compile(
        "^220 TYPSoft FTP Server \d+\.\d+(\.\d+)? ready",
        re.IGNORECASE
        )
    version_re = re.compile(
        "Server (\d+(?:\.\d+)*) ready",
        re.IGNORECASE
        )

    tests = {
        "FtpTypSoft_1": {
            "local_metadata": {
                "product": "TYPSoft FTPd",
                "version": "1.10"
            }
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.impl_re.search(banner):
            meta.local_metadata.product = "TYPSoft FTPd"

            version = self.version_re.search(banner).group(1)
            meta.local_metadata.version = version

            return meta

    """ Tests
    "220 TYPSoft FTP Server 1.10 ready...\r\n"
    "220 TYPSoft FTP Server 1.11 ready...\r\n"
    "220 TYPSoft FTP Server 1.10 ready...\r\n"
    "220 TYPSoft FTP Server 1.10 ready...\r\n"
    "220 TYPSoft FTP Server 1.10 ready...\r\n"
    "220 TYPSoft FTP Server 1.10 ready...\r\n"
    "220 TYPSoft FTP Server 1.10 ready...\r\n"
    "220 TYPSoft FTP Server 1.10 ready...\r\n"
    "220 TYPSoft FTP Server 1.10 ready...\r\n"
    "220 TYPSoft FTP Server 1.11 ready...\r\n"
    "220 TYPSoft FTP Server 1.10 ready...\r\n"
    "220 TYPSoft FTP Server 1.10 ready...\r\n"
    "220 TYPSoft FTP Server 1.11 ready...\r\n"
    "220 TYPSoft FTP Server 1.10 ready...\r\n"
    """
