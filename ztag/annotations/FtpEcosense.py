import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpEcosense(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    ecosense_re = re.compile(
                        "^220  ADH FTP SERVER READY TYPE HELP FOR HELP",
                        re.IGNORECASE
                        )

    def process(self, obj, meta):
        banner = obj["banner"]
        tagged = False

        if self.ecosense_re.search(banner):
            meta.global_metadata.device_type = Type.DVR
            meta.global_metadata.manufacturer = Manufacturer.DEDICATED_MICROS
            tagged = True

        if tagged:
            return meta
        else:
            return None

    """ Tests
    "220  ADH FTP SERVER READY TYPE HELP FOR HELP \r\n"
    "220  ADH FTP SERVER READY TYPE HELP FOR HELP \r\n"
    "220  ADH FTP SERVER READY TYPE HELP FOR HELP \r\n"
    "220  ADH FTP SERVER READY TYPE HELP FOR HELP \r\n"
    "220  ADH FTP SERVER READY TYPE HELP FOR HELP \r\n"
    "220  ADH FTP SERVER READY TYPE HELP FOR HELP \r\n"
    "220  ADH FTP SERVER READY TYPE HELP FOR HELP \r\n"
    "220  ADH FTP SERVER READY TYPE HELP FOR HELP \r\n"
    "220  ADH FTP SERVER READY TYPE HELP FOR HELP \r\n"
    "220  ADH FTP SERVER READY TYPE HELP FOR HELP \r\n"
    "220  ADH FTP SERVER READY TYPE HELP FOR HELP \r\n"
    "220  ADH FTP SERVER READY TYPE HELP FOR HELP \r\n"
    "220  ADH FTP SERVER READY TYPE HELP FOR HELP \r\n"
    "220  ADH FTP SERVER READY TYPE HELP FOR HELP \r\n"
    """
