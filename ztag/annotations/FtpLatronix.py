from ztag.annotation import Annotation
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test
import re


class FtpLatronix(Annotation):
    name = "Latronix"
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    product_re = re.compile(
        "^220 FTP Version (\d+\.\d+) on EPS2-100",
        re.IGNORECASE
        )

    tests = {
        "FtpLatronix_1": {
            "global_metadata": {
                "device_type": Type.PRINT_SERVER,
                "manufacturer": Manufacturer.LANTRONIX,
                "product": "EPS2-100"
            },
            "local_metadata": {
                "version": "1.1"
            }
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.product_re.search(banner):
            meta.global_metadata.device_type = Type.PRINT_SERVER
            meta.global_metadata.manufacturer = Manufacturer.LANTRONIX
            meta.global_metadata.product = "EPS2-100"

            version = self.product_re.search(banner).group(1)
            meta.local_metadata.version = version
            return meta
