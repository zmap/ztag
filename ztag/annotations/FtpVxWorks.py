import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag import protocols
import ztag.test


class FtpVxWorks(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    versionStr = "\d+\.\d+(\.\d+)?(([a-z])|(rc\d))?"
    impl_1_re = re.compile(
        "^220 VxWorks FTP server \(VxWorks " + versionStr + "\) ready",
        re.IGNORECASE
        )
    impl_2_re = re.compile(
        "^220 VxWorks \((VxWorks)?( )?" + versionStr + "(-[A-Z])?\) FTP server ready",
        re.IGNORECASE
        )

    version_re = re.compile(
        "\((?:VxWorks)?(?: )?(\d+(\.\d+)*)\)",
        re.IGNORECASE
        )

    tests = {
        "FtpVxWorks_1": {
            "local_metadata": {
                "product": "VxWorks",
                "version": "5.4.2"
            }
        },
        "FtpVxWorks_2": {
            "local_metadata": {
                "product": "VxWorks",
                "version": "5.4"
            }
        },
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if (
            self.impl_1_re.search(banner) or
            self.impl_2_re.search(banner)
        ):
            meta.local_metadata.product = "VxWorks"

            version = self.version_re.search(banner).group(1)
            meta.local_metadata.version = version

        return meta

    """ Tests
    "220 VxWorks (VxWorks5.4.2) FTP server ready\r\n"
    "220 VxWorks (VxWorks5.5.1) FTP server ready\r\n"
    "220 VxWorks (VxWorks5.4.2) FTP server ready\r\n"
    "220 VxWorks (VxWorks5.5.1) FTP server ready\r\n"
    "220 VxWorks (VxWorks5.4.2) FTP server ready\r\n"
    "220 VxWorks (5.4) FTP server ready\r\n"
    "220 VxWorks (5.4) FTP server ready\r\n"
    "220 VxWorks (VxWorks5.4.2) FTP server ready\r\n"
    "220 VxWorks (5.4) FTP server ready\r\n"
    "220 VxWorks (VxWorks5.5) FTP server ready\r\n"
    "220 VxWorks (VxWorks5.4.2) FTP server ready\r\n"
    "220 VxWorks (VxWorks5.5.1) FTP server ready\r\n"
    "220 VxWorks (VxWorks5.4.2) FTP server ready\r\n"
    "220 VxWorks (5.4) FTP server ready\r\n"
    "220 VxWorks (VxWorks5.5.1) FTP server ready\r\n"
    "220 VxWorks (5.4) FTP server ready\r\n"
    "220 VxWorks (5.4) FTP server ready\r\n"
    "220 VxWorks (VxWorks5.4.2) FTP server ready\r\n"
    "220 VxWorks (VxWorks5.5.1) FTP server ready\r\n"
    "220 VxWorks (VxWorks5.5.1) FTP server ready\r\n"
    "220 VxWorks (VxWorks5.5.1) FTP server ready\r\n"
    "220 VxWorks (5.4) FTP server ready\r\n"
    "220 VxWorks (VxWorks5.5.1) FTP server ready\r\n"
    "220 VxWorks (VxWorks5.4.2) FTP server ready\r\n"
    "220 VxWorks (VxWorks5.5.1) FTP server ready\r\n"
    "220 VxWorks (5.4) FTP server ready\r\n"
    "220 VxWorks (VxWorks5.5.1) FTP server ready\r\n"
    "220 VxWorks (VxWorks5.5.1) FTP server ready\r\n"
    "220 VxWorks (VxWorks5.4.2) FTP server ready\r\n"
    "220 VxWorks (VxWorks5.4.2) FTP server ready\r\n"
    "220 VxWorks (VxWorks5.5) FTP server ready\r\n"
    "220 VxWorks (VxWorks5.4.2) FTP server ready\r\n"
    """
