import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpOpto22(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    manufact_re = re.compile("^220 Opto 22 FTP server ready", re.IGNORECASE)

    tests = {
        "FtpOpto22_1": {
            "global_metadata": {
                "device_type": Type.INDUSTRIAL_CONTROL,
                "manufacturer": Manufacturer.OPTO22
            }
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.manufact_re.search(banner):
            meta.global_metadata.device_type = Type.INDUSTRIAL_CONTROL
            meta.global_metadata.manufacturer = Manufacturer.OPTO22

            return meta

    """ Tests
    "220 Opto 22 FTP server ready.\r\n"
    "220 Opto 22 FTP server ready.\r\n"
    "220 Opto 22 FTP server ready.\r\n"
    "220 Opto 22 FTP server ready.\r\n"
    "220 Opto 22 FTP server ready.\r\n"
    "220 Opto 22 FTP server ready.\r\n"
    "220 Opto 22 FTP server ready.\r\n"
    "220 Opto 22 FTP server ready.\r\n"
    "220 Opto 22 FTP server ready.\r\n"
    "220 Opto 22 FTP server ready.\r\n"
    "220 Opto 22 FTP server ready.\r\n"
    "220 Opto 22 FTP server ready.\r\n"
    "220 Opto 22 FTP server ready.\r\n"
    "220 Opto 22 FTP server ready.\r\n"
    "220 Opto 22 FTP server ready.\r\n"
    "220 Opto 22 FTP server ready.\r\n"
    """
