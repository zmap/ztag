import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag import protocols
import ztag.test


class FtpTelindusFtpd(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    impl_re = re.compile("^220 Telindus FTP server ready", re.IGNORECASE)

    tests = {
        "FtpTelindusFtpd_1": {
            "local_metadata": {
                "product": "Telindus FTPd"
            }
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.impl_re.search(banner):
            meta.local_metadata.product = "Telindus FTPd"

            return meta

    """ Tests
    "220 Telindus FTP server ready.\r\n"
    "220 Telindus FTP server ready.\r\n"
    "220 Telindus FTP server ready.\r\n"
    "220 Telindus FTP server ready.\r\n"
    "220 Telindus FTP server ready.\r\n"
    "220 Telindus FTP server ready.\r\n"
    "220 Telindus FTP server ready.\r\n"
    "220 Telindus FTP server ready.\r\n"
    "220 Telindus FTP server ready.\r\n"
    "220 Telindus FTP server ready.\r\n"
    "220 Telindus FTP server ready.\r\n"
    "220 Telindus FTP server ready.\r\n"
    "220 Telindus FTP server ready.\r\n"
    "220 Telindus FTP server ready.\r\n"
    "220 Telindus FTP server ready.\r\n"
    """
