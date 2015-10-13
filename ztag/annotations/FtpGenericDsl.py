import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpGenericDsl(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    product_re = re.compile("^220 DSL Router FTP Server", re.IGNORECASE)

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.product_re.search(banner):
            meta.global_metadata.device_type = Type.DSL_MODEM

        return meta

    """ Tests
    "220 DSL Router FTP Server v00.96.315 ready\r\n"
    "220 DSL Router FTP Server v02.00.132v4 ready\r\n"
    "220 DSL Router FTP Server v00.96.601 ready\r\n"
    "220 DSL Router FTP Server v00.96.315 ready\r\n"
    "220 DSL Router FTP Server v00.96.315 ready\r\n"
    "220 DSL Router FTP Server v00.96.315 ready\r\n"
    "220 DSL Router FTP Server v00.96.315 ready\r\n"
    "220 DSL Router FTP Server v02.00.132v4 ready\r\n"
    "220 DSL Router FTP Server v00.96.802 ready\r\n"
    "220 DSL Router FTP Server v02.00.132v4 ready\r\n"
    "220 DSL Router FTP Server v02.00.132v4 ready\r\n"
    "220 DSL Router FTP Server v00.96.315 ready\r\n"
    "220 DSL Router FTP Server v00.96.315 ready\r\n"
    "220 DSL Router FTP Server v02.00.132v3W4 ready\r\n"
    "220 DSL Router FTP Server v00.96.315 ready\r\n"
    """
