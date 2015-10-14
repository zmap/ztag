import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpBelkin(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    manufact_re = re.compile(
        "^220 Belkin Network USB Hub Ver \d+\.\d+\.\d+ FTP",
        re.IGNORECASE
        )

    tests = {
        "FtpBelkin_1": {
            "global_metadata": {
                "device_type": Type.USB_HUB,
                "manufacturer": Manufacturer.BELKIN
            }
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]
        tagged = False

        if self.manufact_re.search(banner):
            meta.global_metadata.device_type = Type.USB_HUB
            meta.global_metadata.manufacturer = Manufacturer.BELKIN
            tagged = True

        if tagged:
            return meta
        else:
            return None
