from ztag.annotation import Annotation
from ztag import protocols
import ztag.test
import re


class IQEye(Annotation):
    name = "IQEye"
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    manufact_re = re.compile(
        "^220 FTP Version (\d+\.\d+) on IQeye\d+",
        re.IGNORECASE
        )

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.manufact_re.search(banner):
            meta.global_metadata.device_type = Type.CAMERA
            meta.global_metadata.manufacturer = Manufacturer.IQEYE

            version = self.manufact_re.search(banner).group(1)
            meta.local_metadata.version = version

            return meta

        return None
