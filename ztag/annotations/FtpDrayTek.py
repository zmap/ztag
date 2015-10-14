import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpDrayTek(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None
    manufact_re = re.compile("^220 DrayTek FTP version", re.IGNORECASE)
    version_re = re.compile("FTP version (\d+\.\d+)", re.IGNORECASE)

    tests = {
        "FtpDrayTek_1": {
            "global_metadata": {
                "manufacturer": Manufacturer.DRAYTEK
            },
            "local_metadata": {
                "version": "1.0"
            }
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.manufact_re.search(banner):
            meta.global_metadata.manufacturer = Manufacturer.DRAYTEK
            
            version = self.version_re.search(banner).group(1)
            meta.local_metadata.version = version
            return meta

    """ Tests
    "220 DrayTek FTP version 1.0\r\n"
    "220 DrayTek FTP version 1.0\r\n"
    "220 DrayTek FTP version 1.0\r\n"
    "220 DrayTek FTP version 1.0\r\n"
    "220 DrayTek FTP version 1.0\r\n"
    "220 DrayTek FTP version 1.0\r\n"
    "220 DrayTek FTP version 1.0\r\n"
    "220 DrayTek FTP version 1.0\r\n"
    "220 DrayTek FTP version 1.0\r\n"
    "220 DrayTek FTP version 1.0\r\n"
    "220 DrayTek FTP version 1.0\r\n"
    """
