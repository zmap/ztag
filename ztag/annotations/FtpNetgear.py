import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpNetgear(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    version_re = re.compile(
        "ProFTPD (\d+\.\d+\.\d+)([a-z])? Server",
        re.IGNORECASE
        )

    tests = {
        "FtpNetGear_1": {
            "global_metadata": {
                "device_type": Type.NAS,
                "manufacturer": Manufacturer.NETGEAR,
                "product": "ReadyNAS"
            },
            "local_metadata": {
                "product": "ProFTPD",
                "version": "1.3.3",
                "revision": "g"
            }
        }
    }


    def process(self, obj, meta):
        banner = obj["banner"]

        if "(NETGEAR ReadyNAS)" in banner:
            meta.global_metadata.device_type = Type.NAS
            meta.global_metadata.manufacturer = Manufacturer.NETGEAR
            meta.global_metadata.product = "ReadyNAS"

            if banner.startswith("220 ProFTPD"):
                meta.local_metadata.product = "ProFTPD"

                version = self.version_re.search(banner).group(1)
                meta.local_metadata.version = version

                rev = self.version_re.search(banner).group(2)
                meta.local_metadata.revision = rev

        return meta

    """ Tests
    "220 ProFTPD 1.3.5 Server (NETGEAR ReadyNAS) [::ffff:192.168.1.112]\r\n"
    "220 ProFTPD 1.3.3c Server (NETGEAR ReadyNAS) [192.168.0.88]\r\n"
    "220 ProFTPD 1.3.3g Server (NETGEAR ReadyNAS) [::ffff:192.168.1.134]\r\n"
    "220 ProFTPD 1.3.3g Server (NETGEAR ReadyNAS) [192.168.0.3]\r\n"
    "220 ProFTPD 1.3.3g Server (NETGEAR ReadyNAS) [192.168.1.80]\r\n"
    "220 ProFTPD 1.3.3g Server (NETGEAR ReadyNAS) [192.168.19.23]\r\n"
    "220 ProFTPD 1.3.3g Server (NETGEAR ReadyNAS) [192.168.0.10]\r\n"
    "220 ProFTPD 1.3.5 Server (NETGEAR ReadyNAS) [::ffff:192.168.0.2]\r\n"
    "220 ProFTPD 1.3.5 Server (NETGEAR ReadyNAS) [::ffff:192.168.1.50]\r\n"
    "220 ProFTPD 1.3.5 Server (NETGEAR ReadyNAS) [::ffff:192.168.254.70]\r\n"
    "220 ProFTPD 1.3.5 Server (NETGEAR ReadyNAS) [::ffff:192.168.1.250]\r\n"
    "220 ProFTPD 1.3.3g Server (NETGEAR ReadyNAS) [82.69.54.235]\r\n"
    "220 ProFTPD 1.3.3g Server (NETGEAR ReadyNAS) [192.168.1.5]\r\n"
    "220 ProFTPD 1.3.3g Server (NETGEAR ReadyNAS) [192.168.1.90]\r\n"
    "220 ProFTPD 1.3.3c Server (NETGEAR ReadyNAS) [10.1.2.13]\r\n"
    """
