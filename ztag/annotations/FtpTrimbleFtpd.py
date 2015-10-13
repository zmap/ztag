from ztag.annotation import Annotation
from ztag import protocols
import ztag.test


class Trimble(Annotation):
    name = "Trimble"
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    def process(self, obj, meta):
        banner = obj["banner"]

        if banner.startswith("220 Trimble FTP server (Trimble) ready"):
            meta.local_metadata.product = "Trimble"

        return meta
