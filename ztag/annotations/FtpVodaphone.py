import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpVodaphone(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    versionStr = "\d+\.\d+(\.\d+)?(([a-z])|(rc\d))?"
    manufact_re = re.compile(
        "^220 DSL-EasyBox \d+ FTP Server v" + versionStr + " ready",
        re.IGNORECASE
        )

    product_re = re.compile("^220 DSL-(EasyBox \d+) FTP", re.IGNORECASE)
    version_re = re.compile("Server v(\d+(?:\.\d+)+) ", re.IGNORECASE)

    tests = {
        "FtpVodaphone_1": {
            "global_metadata": {
                "device_type": Type.DSL_MODEM,
                "manufacturer": Manufacturer.VODAPHONE,
                "product": "EasyBox 802",
            },
            "local_metadata": {
                "version": "20.02.240"
            }
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.manufact_re.search(banner):
            meta.global_metadata.device_type = Type.DSL_MODEM
            meta.global_metadata.manufacturer = Manufacturer.VODAPHONE

            product = self.product_re.search(banner).group(1)
            meta.global_metadata.product = product

            version = self.version_re.search(banner).group(1)
            meta.local_metadata.version = version

            return meta

    """ Tests
    "220 DSL-EasyBox 802 FTP Server v20.02.235 ready\r\n"
    "220 DSL-EasyBox 802 FTP Server v20.02.236 ready\r\n"
    "220 DSL-EasyBox 802 FTP Server v20.02.236 ready\r\n"
    "220 DSL-EasyBox 803 FTP Server v30.05.225 ready\r\n"
    "220 DSL-EasyBox 803 FTP Server v30.05.225 ready\r\n"
    "220 DSL-EasyBox 802 FTP Server v20.02.236 ready\r\n"
    "220 DSL-EasyBox 803 FTP Server v30.05.225 ready\r\n"
    "220 DSL-EasyBox 803 FTP Server v30.05.225 ready\r\n"
    "220 DSL-EasyBox 803 FTP Server v30.05.225 ready\r\n"
    "220 DSL-EasyBox 803 FTP Server v30.05.225 ready\r\n"
    "220 DSL-EasyBox 803 FTP Server v30.05.219 ready\r\n"
    "220 DSL-EasyBox 802 FTP Server v20.02.235 ready\r\n"
    "220 DSL-EasyBox 803 FTP Server v30.05.225 ready\r\n"
    "220 DSL-EasyBox 802 FTP Server v20.02.240 ready\r\n"
    "220 DSL-EasyBox 803 FTP Server v30.05.225 ready\r\n"
    "220 DSL-EasyBox 803 FTP Server v30.05.225 ready\r\n"
    "220 DSL-EasyBox 802 FTP Server v20.02.236 ready\r\n"
    "220 DSL-EasyBox 803 FTP Server v30.05.225 ready\r\n"
    "220 DSL-EasyBox 803 FTP Server v30.05.225 ready\r\n"
    "220 DSL-EasyBox 803 FTP Server v30.05.225 ready\r\n"
    "220 DSL-EasyBox 803 FTP Server v30.05.225 ready\r\n"
    "220 DSL-EasyBox 803 FTP Server v30.05.225 ready\r\n"
    "220 DSL-EasyBox 803 FTP Server v30.05.221 ready\r\n"
    "220 DSL-EasyBox 803 FTP Server v30.05.225 ready\r\n"
    "220 DSL-EasyBox 803 FTP Server v30.05.225 ready\r\n"
    """
