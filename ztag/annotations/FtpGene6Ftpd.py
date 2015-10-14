import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag import protocols
import ztag.test


class FtpGene6Ftpd(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    versionStr = "\d+\.\d+(\.\d+)?(([a-z])|(rc\d))?"
    impl_re = re.compile(
        "Gene6[- ]FTP Server v" + versionStr + " +\(Build \d+\)",
        re.IGNORECASE
        )
    version_re = re.compile(
        "FTP Server v(\d+\.\d+\.\d+) \((.+)\)",
        re.IGNORECASE
        )

    tests = {
        "FtpGene6Ftpd_1": {
            "global_metadata": {
                "os": OperatingSystem.WINDOWS,
            },
            "local_metadata": {
                "product": "Gene6 FTP",
                "version": "3.10.0",
                "revision": "Build 2"
            }
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.impl_re.search(banner):
            meta.global_metadata.os = OperatingSystem.WINDOWS

            meta.local_metadata.product = "Gene6 FTP"

            version = self.version_re.search(banner).group(1)
            meta.local_metadata.version = version

            rev = self.version_re.search(banner).group(2)
            meta.local_metadata.revision = rev
            return meta

    """ Tests
    "220 Gene6 FTP Server v3.10.0 (Build 2) ready...\r\n"
    "220 Gene6 FTP Server v3.10.0 (Build 2) ready...\r\n"
    "220 Gene6 FTP Server v3.10.0 (Build 2) ready...\r\n"
    "220 Gene6 FTP Server v3.8.0 (Build 34) ready...\r\n"
    "220 Gene6 FTP Server v3.10.0 (Build 2) ready...\r\n"
    "220 Gene6 FTP Server v3.10.0 (Build 2) ready...\r\n"
    "220 Gene6 FTP Server v3.10.0 (Build 2) ready...\r\n"
    "220 Gene6 FTP Server v3.10.0 (Build 2) ready...\r\n"
    "220 Gene6 FTP Server v3.8.0 (Build 34) ready...\r\n"
    "220 Gene6 FTP Server v3.10.0 (Build 2) ready...\r\n"
    "220 Gene6 FTP Server v3.8.0 (Build 34) ready...\r\n"
    "220 Gene6 FTP Server v3.8.0 (Build 34) ready...\r\n"
    "220 Gene6 FTP Server v3.9.0 (Build 2) ready...\r\n"
    "220 Gene6 FTP Server v3.10.0 (Build 2) ready...\r\n"
    "220 Gene6 FTP Server v3.10.0 (Build 2) ready...\r\n"
    "220 Gene6 FTP Server v3.9.0 (Build 2) ready...\r\n"
    "220 Gene6 FTP Server v3.8.0 (Build 34) ready...\r\n"
    "220 Gene6 FTP Server v3.10.0 (Build 2) ready...\r\n"
    "220 Gene6 FTP Server v3.8.0 (Build 34) ready...\r\n"
    "220 Gene6 FTP Server v3.8.0 (Build 34) ready...\r\n"
    """
