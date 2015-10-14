import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpSpeedPort(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    manufact_re = re.compile("^220 Speedport( )?W", re.IGNORECASE)
    product_re = re.compile("^220 Speedport (.+) FTP Server", re.IGNORECASE)
    impl_re = re.compile("FTP Server v(\d+(?:\.\d+)*) ready", re.IGNORECASE)

    tests = {
        "FtpSpeedPort_1": {
            "global_metadata": {
                "device_type": Type.SOHO_ROUTER,
                "manufacturer": Manufacturer.SPEEDPORT,
                "product": "W 723V Typ B",
            },
            "local_metadata": {
                "version": "1.37.000"
            }
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.manufact_re.search(banner):
            meta.global_metadata.device_type = Type.SOHO_ROUTER
            meta.global_metadata.manufacturer = Manufacturer.SPEEDPORT

            product = self.product_re.search(banner).group(1)
            meta.global_metadata.product = product

            version = self.impl_re.search(banner).group(1)
            meta.local_metadata.version = version

            return meta

    """ Tests
    "220 Speedport W 723V Typ B FTP Server v1.37.000 ready\r\n"
    "220 Speedport W 723V Typ B FTP Server v1.37.000 ready\r\n"
    "220 Speedport W 504V Typ A FTP Server v1.17.000 ready\r\n"
    "220 Speedport W 723V Typ B FTP Server v1.37.000 ready\r\n"
    "220 Speedport W 723V Typ B FTP Server v1.37.000 ready\r\n"
    "220 Speedport W 921V FTP Server v1.37.000 ready\r\n"
    "220 Speedport W 723V Typ B FTP Server v1.37.000 ready\r\n"
    "220 Speedport W 723V Typ B FTP Server v1.37.000 ready\r\n"
    "220 Speedport W 921V FTP Server v1.37.000 ready\r\n"
    "220 Speedport W 723V Typ B FTP Server v1.37.000 ready\r\n"
    "220 Speedport W 723V Typ B FTP Server v1.37.000 ready\r\n"
    "220 Speedport W 504V Typ A FTP Server v1.17.000 ready\r\n"
    "220 Speedport W 504V Typ A FTP Server v1.17.000 ready\r\n"
    "220 Speedport W 921V FTP Server v1.37.000 ready\r\n"
    "220 Speedport W 723V Typ B FTP Server v1.37.000 ready\r\n"
    "220 Speedport W 723V Typ B FTP Server v1.37.000 ready\r\n"
    """
