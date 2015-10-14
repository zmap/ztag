import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpOverlandStorage(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    version_re = re.compile(
        "ProFTPD (\d+\.\d+\.\d+)([a-z])? Server",
        re.IGNORECASE
        )

    tests = {
        "FtpOverlandStorage_1": {
            "global_metadata": {
                "device_type": Type.NAS,
                "manufacturer": Manufacturer.OVERLAND_STORAGE,
                "product": "Snap Appliance"
            },
            "local_metadata": {
                "product": "ProFTPD",
                "version": "1.2.9"
            }
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if "(Snap Appliance FTP Server)" in banner:
            meta.global_metadata.device_type = Type.NAS
            meta.global_metadata.manufacturer = Manufacturer.OVERLAND_STORAGE
            meta.global_metadata.product = "Snap Appliance"

            if banner.startswith("220 ProFTPD"):
                meta.local_metadata.product = "ProFTPD"

                version = self.version_re.search(banner).group(1)
                meta.local_metadata.version = version

                rev = self.version_re.search(banner).group(2)
                meta.local_metadata.revision = rev

        return meta

    """ Tests
    "220 ProFTPD 1.2.9 Server (Snap Appliance FTP Server) [SNAP2252876.spec.local]\r\n"
    "220 ProFTPD 1.2.9 Server (Snap Appliance FTP Server) [HAFServer.uconn.edu]\r\n"
    """
