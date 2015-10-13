import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpGenericCamera(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    dev_type_re = re.compile(
        "^220 Network-Camera FTP server \((.*)\) ready",
        re.IGNORECASE
        )
    version_re = re.compile(
        "^220 Network-Camera FTP server \((.*)\) ready",
        re.IGNORECASE
        )

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.dev_type_re.search(banner):
            meta.global_metadata.device_type = Type.CAMERA
            version = self.version_re.search(banner).group(1)
            if version.lower.startswith("version"):
                meta.local_metadata.product = version.split("/")[-1]
                meta.local_metadata.version = version.split("/")[0]
            elif version.lower.startswith("gnu"):
                temp = version.split(" ")[0:1]
                meta.local_metadata.product = " ".join(temp)
                meta.local_metadata.version = version.split(" ")[2]

        return meta

    """ Tests
    "220 Network-Camera FTP server (Version 6.4/OpenBSD/Linux-ftpd-0.17) ready.\r\n"
    "220 Network-Camera FTP server (GNU inetutils 1.4.2) ready.\r\n"
    "220 Network-Camera FTP server (Version 6.4/OpenBSD/Linux-ftpd-0.17) ready.\r\n"
    "220 Network-Camera FTP server (Version 6.4/OpenBSD/Linux-ftpd-0.17) ready.\r\n"
    "220 Network-Camera FTP server (GNU inetutils 1.4.2) ready.\r\n"
    "220 Network-Camera FTP server (GNU inetutils 1.4.2) ready.\r\n"
    "220 Network-Camera FTP server (GNU inetutils 1.4.2) ready.\r\n"
    "220 Network-Camera FTP server (GNU inetutils 1.4.2) ready.\r\n"
    "220 Network-Camera FTP server (GNU inetutils 1.4.2) ready.\r\n"
    "220 Network-Camera FTP server (GNU inetutils 1.4.2) ready.\r\n"
    "220 Network-Camera FTP server (Version 6.4/OpenBSD/Linux-ftpd-0.17) ready.\r\n"
    "220 Network-Camera FTP server (Version 6.4/OpenBSD/Linux-ftpd-0.17) ready.\r\n"
    "220 Network-Camera FTP server (Version 6.4/OpenBSD/Linux-ftpd-0.17) ready.\r\n"
    "220 Network-Camera FTP server (Version 6.4/OpenBSD/Linux-ftpd-0.17) ready.\r\n"
    """
