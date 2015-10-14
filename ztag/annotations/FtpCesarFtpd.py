import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag import protocols
import ztag.test


class FtpCesarFtpd(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    impl_re = re.compile("^220[- ]CesarFTP 0\.\d+", re.IGNORECASE)
    version_re = re.compile("CesarFTP (\d+\.\d+)([a-z])?", re.IGNORECASE)

    tests = {
        "FtpCesarFtpd_1": {
            "global_metadata": {
                "os": OperatingSystem.WINDOWS,
            },
            "local_metadata": {
                "product": "Cesar FTP",
                "version": "0.99",
                "revision": "g"
            }
        }
    }


    def process(self, obj, meta):
        banner = obj["banner"]

        if self.impl_re.search(banner):
            meta.global_metadata.os = OperatingSystem.WINDOWS

            meta.local_metadata.product = "Cesar FTP"

            version = self.version_re.search(banner).group(1)
            meta.local_metadata.version = version

            rev = self.version_re.search(banner).group(2)
            meta.local_metadata.revision = rev

        return meta

    """ Tests
    "220 CesarFTP 0.99g Server Welcome !\r\n"
    "220 CesarFTP 0.99g Server Welcome !\r\n"
    "220 CesarFTP 0.99g Server Welcome !\r\n"
    "220 CesarFTP 0.99g Server Welcome !\r\n"
    "220 CesarFTP 0.99g Server Welcome !\r\n"
    "220 CesarFTP 0.99g Server Welcome !\r\n"
    "220 CesarFTP 0.99g Server Welcome !\r\n"
    "220 CesarFTP 0.99g Server Welcome !\r\n"
    "220 CesarFTP 0.99g Server Welcome !\r\n"
    "220 CesarFTP 0.99g Server Welcome !\r\n"
    """
