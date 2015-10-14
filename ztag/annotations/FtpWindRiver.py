import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpWindRiver(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    manufact_re = re.compile("^220 Wind River FTP server", re.IGNORECASE)
    version_re = re.compile("FTP server (\d+\.\d+) ready", re.IGNORECASE)

    tests = {
        "FtpWindRiver_1": {
            "global_metadata": {
                "device_type": Type.SOHO_ROUTER,
                "manufacturer": Manufacturer.WIND_RIVER,
            },
            "local_metadata": {
                "version": "6.5"
            }
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.manufact_re.search(banner):
            meta.global_metadata.device_type = Type.SOHO_ROUTER
            meta.global_metadata.manufacturer = Manufacturer.WIND_RIVER

            version = self.version_re.search(banner).group(1)
            meta.local_metadata.version = version

            return meta

    """ Tests
    "220 Wind River FTP server 6.5 ready.\r\n"
    "220 Wind River FTP server 6.5 ready.\r\n"
    "220 Wind River FTP server 6.5 ready.\r\n"
    "220 Wind River FTP server 6.5 ready.\r\n"
    "220 Wind River FTP server 6.5 ready.\r\n"
    "220 Wind River FTP server 6.5 ready.\r\n"
    "220 Wind River FTP server 6.5 ready.\r\n"
    "220 Wind River FTP server 6.5 ready.\r\n"
    "220 Wind River FTP server 6.5 ready.\r\n"
    "220 Wind River FTP server 6.5 ready.\r\n"
    "220 Wind River FTP server 6.5 ready.\r\n"
    "220 Wind River FTP server 6.5 ready.\r\n"
    "220 Wind River FTP server 6.5 ready.\r\n"
    "220 Wind River FTP server 6.5 ready.\r\n"
    "220 Wind River FTP server 6.5 ready.\r\n"
    "220 Wind River FTP server 6.5 ready.\r\n"
    "220 Wind River FTP server 6.5 ready.\r\n"
    """
