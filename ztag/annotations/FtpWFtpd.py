import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag import protocols
import ztag.test


class FtpWFtpd(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None
    impl_re = re.compile(
        "^220 WFTPD \d+\.\d+ service \(by Texas Imperial Software\) ready for new user",
        re.IGNORECASE
        )
    version_re = re.compile("WFTPD (\d+\.\d+) service", re.IGNORECASE)

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.impl_re.search(banner):
            meta.local_metadata.product = "WFTPD"
            version = self.version_re.search(banner).group(1)
            meta.local_metadata.version = version

    """ Tests
    "220 WFTPD 3.2 service (by Texas Imperial Software) ready for new user\r\n"
    "220 WFTPD 2.4 service (by Texas Imperial Software) ready for new user\r\n"
    "220 WFTPD 2.30 service (by Texas Imperial Software) ready for new user\r\n"
    "220 WFTPD 3.3 service (by Texas Imperial Software) ready for new user\r\n"
    "220 WFTPD 3.3 service (by Texas Imperial Software) ready for new user\r\n"
    "220 WFTPD 3.3 service (by Texas Imperial Software) ready for new user\r\n"
    "220 WFTPD 3.2 service (by Texas Imperial Software) ready for new user\r\n"
    "220 WFTPD 3.0 service (by Texas Imperial Software) ready for new user\r\n"
    "220 WFTPD 3.2 service (by Texas Imperial Software) ready for new user\r\n"
    "220 WFTPD 3.3 service (by Texas Imperial Software) ready for new user\r\n"
    "220 WFTPD 3.3 service (by Texas Imperial Software) ready for new user\r\n"
    "220 WFTPD 3.3 service (by Texas Imperial Software) ready for new user\r\n"
    "220 WFTPD 3.2 service (by Texas Imperial Software) ready for new user\r\n"
    "220 WFTPD 3.2 service (by Texas Imperial Software) ready for new user\r\n"
    """
