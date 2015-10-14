from ztag.annotation import Annotation
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test
import re


class FtpIQEye(Annotation):
    name = "IQEye"
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    manufact_re = re.compile(
        "^220 FTP Version (\d+\.\d+) on (IQeye\d+)",
        re.IGNORECASE
        )

    tests = {
        "FtpIqeye_1": {
            "global_metadata": {
                "device_type": Type.CAMERA,
                "manufacturer": Manufacturer.IQEYE,
                "product": "IQeye510"
            },
            "local_metadata": {
                "version": "1.1"
            }
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.manufact_re.search(banner):
            meta.global_metadata.device_type = Type.CAMERA
            meta.global_metadata.manufacturer = Manufacturer.IQEYE

            match = self.manufact_re.search(banner)
            meta.local_metadata.version = match.group(1)
            meta.global_metadata.product = match.group(2)

            return meta

        return None
