import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpLutron(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    manufact_re = re.compile(
        "^220\ Welcome\ to\ the\ HomeWorks\ Processor",
        re.IGNORECASE
        )

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.manufact_re.search(banner):
            meta.global_metadata.manufacturer = Manufacturer.LUTRON
            meta.global_metadata.product = "HomeWorks Processor"

        return meta

    """ Tests
    "220 Welcome to the HomeWorks Processor\r\n"
    "220 Welcome to the HomeWorks Processor\r\n"
    "220 Welcome to the HomeWorks Processor\r\n"
    "220 Welcome to the HomeWorks Processor\r\n"
    "220 Welcome to the HomeWorks Processor\r\n"
    "220 Welcome to the HomeWorks Processor\r\n"
    "220 Welcome to the HomeWorks Processor\r\n"
    "220 Welcome to the HomeWorks Processor\r\n"
    "220 Welcome to the HomeWorks Processor\r\n"
    "220 Welcome to the HomeWorks Processor\r\n"
    "220 Welcome to the HomeWorks Processor\r\n"
    "220 Welcome to the HomeWorks Processor\r\n"
    "220 Welcome to the HomeWorks Processor\r\n"
    "220 Welcome to the HomeWorks Processor\r\n"
    "220 Welcome to the HomeWorks Processor\r\n"
    "220 Welcome to the HomeWorks Processor\r\n"
    """
