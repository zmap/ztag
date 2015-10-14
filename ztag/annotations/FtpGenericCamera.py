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

    tests = {
        "FtpGenericCamera_1": {
            "global_metadata": {
                "device_type": Type.CAMERA,
            },
            "local_metadata": {
                "product": "Linux-ftpd-0.17",
                "version": "6.4"
            }
        },
        "FtpGenericCamera_2": {
            "global_metadata": {
                "device_type": Type.CAMERA,
            },
            "local_metadata": {
                "product": "GNU inetutils",
                "version": "1.4.2"
            }
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.dev_type_re.search(banner):
            meta.global_metadata.device_type = Type.CAMERA

            version = self.version_re.search(banner).group(1)
            if version.startswith("Version"):
                meta.local_metadata.product = version.split("/")[-1]
                temp = " ".join(version.split("/")[0].split(" ")[1:])
                meta.local_metadata.version = temp
            elif version.startswith("GNU"):
                temp = version.split(" ")[0:2]
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
