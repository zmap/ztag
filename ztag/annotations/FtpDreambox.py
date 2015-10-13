import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpDreambox(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    open_dreambox_re = re.compile(
                        "^220 Welcome to the OpenDreambox FTP service",
                        re.IGNORECASE
                        )
    dreambox_re = re.compile(
                        "^220 Willkomen auf Ihrer Dreambox.",
                        re.IGNORECASE
                        )

    def process(self, obj, meta):
        banner = obj["banner"]
        tagged = False

        if self.open_dreambox_re.search(banner):
            meta.global_metadata.device_type = Type.TV_BOX
            meta.global_metadata.manufacturer = Manufacturer.DREAMBOX
            meta.tags.append("Uses OpenDreambox")
            tagged = True

        if self.dreambox_re.search(banner):
            meta.global_metadata.device_type = Type.TV_BOX
            meta.global_metadata.manufacturer = Manufacturer.DREAMBOX
            tagged = True

        if tagged:
            return meta
        else:
            return None

    """ Tests
    "220 Welcome to the OpenDreambox FTP service.\r\n"
    "220 Welcome to the OpenDreambox FTP service.\r\n"
    "220 Welcome to the OpenDreambox FTP service.\r\n"
    "220 Willkomen auf Ihrer Dreambox.\r\n"
    "220 Willkomen auf Ihrer Dreambox.\r\n"
    "220 Welcome to the PLi dreambox FTP server\r\n"
    "220 Willkomen auf Ihrer Dreambox.\r\n"
    "220 Welcome to the PLi dreambox FTP server\r\n"
    "220 Willkomen auf Ihrer Dreambox.\r\n"
    "220 Welcome to the OpenDreambox FTP service.\r\n"
    "220 Welcome to the OpenDreambox FTP service.\r\n"
    """
