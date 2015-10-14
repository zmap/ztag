import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag import protocols
import ztag.test


class FtpWarFtpd(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    impl_re = re.compile("WarFTPd \d+\.\d+", re.IGNORECASE)
    version_re = re.compile("WarFTPd (\d+(\.\d+)*)", re.IGNORECASE)

    tests = {
        "FtpWarFtpd_1": {
            "local_metadata": {
                "product": "WarFtpd",
                "version": "1.82.00",
            }
        },
        "FtpWarFtpd_2": {
            "local_metadata": {
                "product": "WarFtpd",
                "version": "1.65",
            }
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.impl_re.search(banner):
            meta.local_metadata.product = "WarFtpd"

            version = self.version_re.search(banner).group(1)
            meta.local_metadata.version = version

            return meta

    """ Tests
    "220-www1.powerweb.net\r\n    WarFTPd 1.82.00-RC11 (Sep 22 2006) Ready\r\n    (C)opyright 1996 - 2006 by Jarle (jgaa) Aase - all rights reserved.\r\n220 Please enter your user name.\r\n"
    "220 ---freeFTPd 1.0---warFTPd 1.65---\r\n"
    "220-SPC FTP\r\n    WarFTPd 1.82.00-RC13 (Sep 12 2009) Ready\r\n    (C)opyright 1996 - 2009 by Jarle (jgaa) Aase - all rights reserved.\r\n220 Please enter your user name.\r\n"
    "220 ---freeFTPd 1.0---warFTPd 1.65---\r\n"
    "220 ---freeFTPd 1.0---warFTPd 1.65---\r\n"
    "220 ---freeFTPd 1.0---warFTPd 1.65---\r\n"
    "220 ---freeFTPd 1.0---warFTPd 1.65---\r\n"
    "220 ---freeFTPd 1.0---warFTPd 1.65---\r\n"
    "220 ---freeFTPd 1.0---warFTPd 1.65---\r\n"
    "220 ---freeFTPd 1.0---warFTPd 1.65---\r\n"
    "220 ---freeFTPd 1.0---warFTPd 1.65---\r\n"
    "220 ---freeFTPd 1.0---warFTPd 1.65---\r\n"
    "220 ---freeFTPd 1.0---warFTPd 1.65---\r\n"
    "220 ---freeFTPd 1.0---warFTPd 1.65---\r\n"
    "220 ---freeFTPd 1.0---warFTPd 1.65---\r\n"
    "220 ---freeFTPd 1.0---warFTPd 1.65---\r\n"
    "220 ---freeFTPd 1.0---warFTPd 1.65---\r\n"
    "220-Jgaa's Fan Club FTP service\r\n    WarFTPd 1.82.00-RC10 (Jan 25 2005) Ready\r\n    (C)opyright 1996 - 2005 by Jarle (jgaa) Aase - all rights reserved.\r\n220 Please enter your user name.\r\n"
    "220 ---freeFTPd 1.0---warFTPd 1.65---\r\n"
    "220 ---freeFTPd 1.0---warFTPd 1.65---\r\n"
    """
