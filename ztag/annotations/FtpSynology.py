import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpSynology(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    manufact_1_re = re.compile("synology", re.IGNORECASE)

    manufact_2_re = re.compile(
        "^220 .*DiskStation(-)?(\d+)? FTP server ready",
        re.IGNORECASE
        )
    manufact_3_re = re.compile(
        "^220 Disk Station FTP server at",
        re.IGNORECASE
        )

    tests = {
        "FtpSynology_1": {
            "global_metadata": {
                "device_type": Type.NAS,
                "manufacturer": Manufacturer.SYNOLOGY,
                "product": "DiskStation"
            }
        },
        "FtpSynology_2": {
            "global_metadata": {
                "device_type": Type.NAS,
                "manufacturer": Manufacturer.SYNOLOGY,
                "product": "Cube Station"
            }
        },
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if (
            self.manufact_2_re.search(banner) or
            self.manufact_3_re.search(banner)
        ):
            meta.global_metadata.device_type = Type.NAS
            meta.global_metadata.manufacturer = Manufacturer.SYNOLOGY
            meta.global_metadata.product = "DiskStation"

            return meta

        if banner.startswith("220 Cube Station FTP server"):
            meta.global_metadata.device_type = Type.NAS
            meta.global_metadata.manufacturer = Manufacturer.SYNOLOGY
            meta.global_metadata.product = "Cube Station"

            return meta

        if self.manufact_1_re.search(banner):
            meta.global_metadata.manufacturer = Manufacturer.SYNOLOGY

            return meta

    """ Tests
    "220 DiskStation FTP server ready.\r\n"
    "220 DiskStation FTP server ready.\r\n"
    "220 DiskStation FTP server ready.\r\n"
    "220 DiskStation FTP server ready.\r\n"
    "220 DiskStation FTP server ready.\r\n"
    "220 DiskStation FTP server ready.\r\n"
    "220 DiskStation FTP server ready.\r\n"
    "220 DiskStation FTP server ready.\r\n"
    "220 Cube Station FTP server at server ready.\r\n"
    "220 Cube Station FTP server at StrategaNAS ready.\r\n"
    "220 Cube Station FTP server at GaiaTek ready.\r\n"
    "220 Cube Station FTP server at FileServer ready.\r\n"
    "220 Cube Station FTP server at Cube ready.\r\n"
    "220 Cube Station FTP server at Bathe-NAS ready.\r\n"
    """
