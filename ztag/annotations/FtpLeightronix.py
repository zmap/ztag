from ztag.annotation import Annotation
from ztag import protocols
import ztag.test
import re


class FtpLeightronix(Annotation):
    name = "Leightronix FTP Server"
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    manufact_re = re.compile(
        "^220-lgxftpd V(\d+\.\d+), LEIGHTRONIX, INC\.",
        re.IGNORECASE
        )

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.manufact_re.search(banner):
            meta.global_metadata.manufacturer = Manufacturer.LEIGHTRONIX

            version = self.manufact_re.search(banner).group(1)
            meta.local_metadata.version = version

        return meta
