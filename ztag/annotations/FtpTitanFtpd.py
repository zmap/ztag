import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag import protocols
import ztag.test


class FtpTitanFtpd(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    versionStr = "\d+\.\d+(\.\d+)?(([a-z])|(rc\d))?"
    impl_str = re.compile(
        "^220 Titan FTP Server " + versionStr + " Ready",
        re.IGNORECASE
        )
    version_re = re.compile("Server (\d+\.\d+\.\d+) Ready", re.IGNORECASE)

    tests = {
        "FtpTitanFtpd_1": {
            "global_metadata": {
                "os": OperatingSystem.WINDOWS_SERVER
            },
            "local_metadata": {
                "product": "Titan FTPd",
                "version": "9.22.1634"
            }
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.impl_str.search(banner):
            meta.global_metadata.os = OperatingSystem.WINDOWS_SERVER

            meta.local_metadata.product = "Titan FTPd"

            version = self.version_re.search(banner).group(1)
            meta.local_metadata.version = version

            return meta

    """ Tests
    "220 Titan FTP Server 8.22.1205 Ready.\r\n"
    "220 Titan FTP Server 8.22.1205 Ready.\r\n"
    "220 Titan FTP Server 4.20.263 Ready.\r\n"
    "220 Titan FTP Server 10.46.1872 Ready.\r\n"
    "220 Titan FTP Server 4.02.248 Ready.\r\n"
    "220 Titan FTP Server 8.10.1125 Ready.\r\n"
    "220 Titan FTP Server 9.22.1634 Ready.\r\n"
    "220 Titan FTP Server 7.02.865 Ready.\r\n"
    "220 Titan FTP Server 8.40.1352 Ready.\r\n"
    "220 Titan FTP Server 8.22.1205 Ready.\r\n"
    "220 Titan FTP Server 7.13.903 Ready.\r\n"
    "220 Titan FTP Server 9.00.1562 Ready.\r\n"
    """
