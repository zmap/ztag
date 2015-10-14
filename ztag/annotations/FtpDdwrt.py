import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpDdwrt(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    multi_re = re.compile(
        "^220 ProFTPD (\d+\.\d+\.\d+)(([a-z])|(rc\d+))? Server \(DD-WRT\)",
        re.IGNORECASE
        )

    tests = {
        "FtpDdwrt_1": {
            "global_metadata": {
                "device_type": Type.SOHO_ROUTER,
            },
            "local_metadata": {
                "product": "ProFTPD",
                "version": "1.3.4",
                "revision": "d"
            },
            "tags": ["Running DD-WRT"]
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        match = self.multi_re.search(banner)
        if match:
            meta.global_metadata.device_type = Type.SOHO_ROUTER

            meta.local_metadata.product = "ProFTPD"
            meta.local_metadata.version = match.group(1)
            meta.local_metadata.revision = match.group(2)

            meta.tags.add("Running DD-WRT")

        return meta

    """ Tests
    "220 ProFTPD 1.3.3 Server (DD-WRT) [111.172.247.3]\r\n"
    "220 ProFTPD 1.3.5 Server (DD-WRT) [192.168.11.1]\r\n"
    "220 ProFTPD 1.3.3 Server (DD-WRT) [198.217.126.150]\r\n"
    "220 ProFTPD 1.3.3 Server (DD-WRT) [87.121.57.70]\r\n"
    "220 ProFTPD 1.3.5 Server (DD-WRT) [93.178.87.170]\r\n"
    "220 ProFTPD 1.3.4d Server (DD-WRT) [222.132.215.160]\r\n"
    "220 ProFTPD 1.3.4d Server (DD-WRT) [109.192.245.7]\r\n"
    "220 ProFTPD 1.3.4c Server (DD-WRT) [69.172.159.139]\r\n"
    "220 ProFTPD 1.3.5 Server (DD-WRT) [74.57.203.70]\r\n"
    "220 ProFTPD 1.3.3c Server (DD-WRT) [10.0.0.254]\r\n"
    "220 ProFTPD 1.3.4b Server (DD-WRT) [80.55.125.190]\r\n"
    """
