import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpFullrate(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    manufact_re = re.compile(
        "^220 Fullrate FTP version \d+\.\d+ ready at",
        re.IGNORECASE
        )
    ftp_version_re = re.compile(
        "^220 Fullrate FTP version (\d+\.\d+) ready at",
        re.IGNORECASE
        )

    tests = {
        "FtpFullrate_1": {
            "global_metadata": {
                "device_type": Type.DSL_MODEM,
                "manufacturer": Manufacturer.FULLRATE
            },
            "local_metadata": {
                "version": "1.0"
            }
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.manufact_re.search(banner):
            meta.global_metadata.device_type = Type.DSL_MODEM
            meta.global_metadata.manufacturer = Manufacturer.FULLRATE

            version = self.ftp_version_re.search(banner)
            if version:
                meta.local_metadata.version = version.group(1)

        return meta

    """ Tests
    "220 Fullrate FTP version 1.0 ready at Mon Jun 22 02:33:10 2015\r\n"
    "220 Fullrate FTP version 1.0 ready at Mon Jun 22 02:32:12 2015\r\n"
    "220 Fullrate FTP version 1.0 ready at Mon Jun 22 02:34:15 2015\r\n"
    "220 fullrate FTP version 1.0 ready at Mon Jun 22 02:35:11 2015\r\n"
    "220 Fullrate FTP version 1.0 ready at Mon Jun 22 02:34:39 2015\r\n"
    "220 Fullrate FTP version 1.0 ready at Mon Jun 22 02:35:56 2015\r\n"
    "220 Fullrate FTP version 1.0 ready at Mon Jun 22 02:35:36 2015\r\n"
    "220 Fullrate FTP version 1.0 ready at Mon Jun 22 02:36:03 2015\r\n"
    "220 Fullrate FTP version 1.0 ready at Mon Jun 22 02:36:01 2015\r\n"
    "220 Fullrate FTP version 1.0 ready at Mon Jun 22 02:36:23 2015\r\n"
    "220 Fullrate FTP version 1.0 ready at Mon Jun 22 02:34:34 2015\r\n"
    "220 Fullrate FTP version 1.0 ready at Mon Jun 22 02:36:12 2015\r\n"
    "220 Fullrate FTP version 1.0 ready at Mon Jun 22 02:36:57 2015\r\n"
    "220 Fullrate FTP version 1.0 ready at Mon Jun 22 02:37:06 2015\r\n"
    "220 Fullrate FTP version 1.0 ready at Mon Jun 22 02:36:33 2015\r\n"
    "220 Fullrate FTP version 1.0 ready at Mon Jun 22 02:36:18 2015\r\n"
    "220 Fullrate FTP version 1.0 ready at Mon Jun 22 02:37:33 2015\r\n"
    "220 Fullrate FTP version 1.0 ready at Mon Jun 22 02:37:36 2015\r\n"
    "220 Fullrate FTP version 1.0 ready at Mon Jun 22 02:36:17 2015\r\n"
    "220 Fullrate FTP version 1.0 ready at Mon Jun 22 02:38:22 2015\r\n"
    "220 Fullrate FTP version 1.0 ready at Mon Jun 22 02:35:48 2015\r\n"
    "220 Fullrate FTP version 1.0 ready at Mon Jun 22 02:38:21 2015\r\n"
    """
