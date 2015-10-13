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

    def process(self, obj, meta):
        banner = obj["banner"]
        tagged = False

        if self.manufact_re.search(banner):
            meta.global_metadaa.manufacturer = Manufacturer.DRAYTEK
            tagged = True

        if tagged:
            return meta
        else:
            return None

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
