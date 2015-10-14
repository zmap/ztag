import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag import protocols
import ztag.test


class FtpBftpd(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    versionStr = "\d+\.\d+(\.\d+)?(([a-z])|(rc\d))?"
    impl_1_re = re.compile(
        "^220 bftpd " + versionStr + " at \d+\.\d+\.\d+\.\d+ ready",
        re.IGNORECASE
        )
    version_1_re = re.compile(
        "bftpd (\d+\.\d+) at",
        re.IGNORECASE
        )

    tests = {
        "FtpBftpd_1": {
            "local_metadata": {
                "product": "bftpd",
                "version": "2.2"
            }
        },
        "FtpBftpd_2": {
            "local_metadata": {
                "product": "bftpd",
            }
        },
    }

    impl_2_re = re.compile("^220 \(bftpd\)\r\n$", re.IGNORECASE)

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.impl_1_re.search(banner):
            meta.local_metadata.product = "bftpd"
            version = self.version_1_re.search(banner).group(1)
            meta.local_metadata.version = version

        if self.impl_2_re.search(banner):
            meta.local_metadata.product = "bftpd"

        return meta

    """ Tests
    "220 (bftpd)\r\n"
    "220 bftpd 2.2 at 186.27.181.33 ready.\r\n"
    "220 bftpd 2.2 at 92.101.111.69 ready.\r\n"
    "220 bftpd 2.2 at 190.99.160.80 ready.\r\n"
    "220 (bftpd)\r\n"
    "220 bftpd 2.3 at 0.0.0.0 ready.\r\n"
    "220 bftpd 2.2 at 109.63.172.186 ready.\r\n"
    "220 bftpd 2.2 at 151.74.240.50 ready.\r\n"
    "220 (bftpd)\r\n"
    "220 bftpd 2.2 at 122.177.18.208 ready.\r\n"
    "220 (bftpd)\r\n"
    "220 bftpd 2.2 at 37.138.201.201 ready.\r\n"
    "220 bftpd 2.2 at 178.37.208.162 ready.\r\n"
    "220 bftpd 2.2 at 41.37.47.129 ready.\r\n"
    "220 (bftpd)\r\n"
    "220 (bftpd)\r\n"
    "220 bftpd 2.2 at 5.155.231.250 ready.\r\n"
    "220 bftpd 2.3 at 0.0.0.0 ready.\r\n"
    "220 bftpd 2.2 at 197.88.95.13 ready.\r\n"
    "220 bftpd 2.2 at 95.107.101.10 ready.\r\n"
    "220 bftpd 2.2 at 37.122.113.86 ready.\r\n"
    "220 (bftpd)\r\n"
    """
