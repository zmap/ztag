from ztag.annotation import Annotation
from ztag import protocols
import ztag.test


class FtpTrimbleFtpd(Annotation):
    name = "Trimble"
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    tests = {
        "FtpTrimbleFtpd_1": {
            "local_metadata": {
                "product": "Trimble Ftpd"
            }
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if banner.startswith("220 Trimble FTP server (Trimble) ready"):
            meta.local_metadata.product = "Trimble Ftpd"

            return meta
