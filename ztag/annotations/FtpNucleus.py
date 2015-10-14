from ztag.annotation import Annotation
from ztag import protocols
import ztag.test
import re


class Nucleus(Annotation):
    name = "Nucleus"
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    version_re = re.compile(
        "FTP Server \(Version (\d+\.\d+)\) ready",
        re.IGNORECASE
        )

    tests = {
        "FtpNucleus_1": {
            "local_metadata": {
                "product": "Nucleus",
                "version": "1.7"
            }
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if banner.startswith("220 Nucleus FTP Server"):
            meta.local_metadata.product = "Nucleus"

            version = self.version_re.search(banner).group(1)
            meta.local_metadata.version = version

        return meta
