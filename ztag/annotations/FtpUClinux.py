from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag import protocols
import ztag.test
import re

class UCLinux(Annotation):
    name = "UCLinux"
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    product_re = re.compile(
        "220 uClinux FTP server \(GNU inetutils (\d+(\.\d+)*)\) ready",
        re.IGNORECASE
        )

    version_re = re.compile(
        "\(GNU inetutils (\d+(?:\.\d+)*)\)",
        re.IGNORECASE
        )

    tests = {
        "FtpUClinux_1": {
            "global_metadata": {
                "os": OperatingSystem.UCLINUX,
            },
            "local_metadata": {
                "product": "GNU inetutils",
                "version": "1.4.1"
            }
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.product_re.search(banner):
            meta.global_metadata.os = OperatingSystem.UCLINUX

            meta.local_metadata.product = "GNU inetutils"

            version = self.version_re.search(banner).group(1)
            meta.local_metadata.version = version

            if "ARM7" in banner:
                meta.tags.append("Uses ARM7 chipset")

            return meta
