import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag import protocols
import ztag.test


class FtpMikroTikFtpd(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    impl_re = re.compile("^220 MikroTik FTP server", re.IGNORECASE)
    version_re = re.compile("\(MikroTik (\d+(?:\.\d+)*)\)", re.IGNORECASE)

    tests = {
        "FtpMikroTikFtpd_1": {
            "local_metadata": {
                "product": "MikroTik",
                "version": "2.9.27"
            }
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.impl_re.search(banner):
            meta.local_metadata.product = "MikroTik"

            version = self.version_re.search(banner).group(1)
            meta.local_metadata.version = version

            return meta

    """ Tests
    "220 MikroTik FTP server (MikroTik 3.30) ready\r\n"
    "220 MikroTik FTP server (MikroTik 2.9.27) ready\r\n"
    "220 MikroTik FTP server (MikroTik 3.30) ready\r\n"
    "220 MikroTik FTP server (MikroTik 5.25) ready\r\n"
    "220 MikroTik FTP server (MikroTik 6.7) ready\r\n"
    "220 MikroTik FTP server (MikroTik 6.28) ready\r\n"
    "220 MikroTik FTP server (MikroTik 5.20) ready\r\n"
    "220 MikroTik FTP server (MikroTik 6.28) ready\r\n"
    "220 MikroTik FTP server (MikroTik 5.20) ready\r\n"
    "220 MikroTik FTP server (MikroTik 4.17) ready\r\n"
    "220 MikroTik FTP server (MikroTik 3.30) ready\r\n"
    "220 MikroTik FTP server (MikroTik 5.24) ready\r\n"
    "220 MikroTik FTP server (MikroTik 6.28) ready\r\n"
    "220 MikroTik FTP server (MikroTik 6.7) ready\r\n"
    "220 MikroTik FTP server (MikroTik 6.29.1) ready\r\n"
    "220 MikroTik FTP server (MikroTik 6.17) ready\r\n"
    "220 MikroTik FTP server (MikroTik 6.22) ready\r\n"
    "220 MikroTik FTP server (MikroTik 6.22) ready\r\n"
    "220 MikroTik FTP server (MikroTik 6.18) ready\r\n"
    "220 MikroTik FTP server (MikroTik 5.26) ready\r\n"
    "220 MikroTik FTP server (MikroTik 6.22) ready\r\n"
    "220 MikroTik FTP server (MikroTik 6.27) ready\r\n"
    """
