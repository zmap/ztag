import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpGenericUpdate(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    tests = {
        "FtpGenericUpdate_1": {
            "tags": ["Update utility"]
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if banner.startswith("220 Ftp firmware update utility"):
            meta.tags.add("Update utility")

            return meta

    """ Tests
    "220 Ftp firmware update utility\r\n"
    "220 Ftp firmware update utility\r\n"
    "220 Ftp firmware update utility\r\n"
    "220 Ftp firmware update utility\r\n"
    "220 Ftp firmware update utility\r\n"
    "220 Ftp firmware update utility\r\n"
    "220 Ftp firmware update utility\r\n"
    "220 Ftp firmware update utility\r\n"
    "220 Ftp firmware update utility\r\n"
    """
