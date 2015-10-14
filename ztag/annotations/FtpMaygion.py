import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpMaygion(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    manufactur_re = re.compile(
        "^220 IPCamera FTPServer\(www\.maygion\.com\)",
        re.IGNORECASE
        )

    tests = {
        "FtpMaygion_1": {
            "global_metadata": {
                "device_type": Type.CAMERA,
                "manufacturer": Manufacturer.MAYGION
            }
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.manufactur_re.search(banner):
            meta.global_metadata.device_type = Type.CAMERA
            meta.global_metadata.manufacturer = Manufacturer.MAYGION

            return meta

    """ Tests
    "220 IPCamera FtpServer(www.maygion.com),do NOT change firmware unless you know what you are doing!\r\n"
    "220 IPCamera FtpServer(www.maygion.com),do NOT change firmware unless you know what you are doing!\r\n"
    "220 IPCamera FtpServer(www.maygion.com),do NOT change firmware unless you know what you are doing!\r\n"
    "220 IPCamera FtpServer(www.maygion.com),used for IPCam Repair and upgrade,do NOT change firmware unless you know what you are doing!\r\n"
    "220 IPCamera FtpServer(www.maygion.com),do NOT change firmware unless you know what you are doing!\r\n"
    "220 IPCamera FtpServer(www.maygion.com),used for IPCam Repair and upgrade,do NOT change firmware unless you know what you are doing!\r\n"
    "220 IPCamera FtpServer(www.maygion.com),do NOT change firmware unless you know what you are doing!\r\n"
    "220 IPCamera FtpServer(www.maygion.com),do NOT change firmware unless you know what you are doing!\r\n"
    """
