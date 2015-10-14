from ztag.annotation import Annotation
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test
import re


class FtpNetApp(Annotation):
    name = "NetApp FTP Server"
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    manufact_re = re.compile(
        "^220 .+ FTP server \(NetApp Release",
        re.IGNORECASE
        )

    version_re = re.compile(
        "^220 .+ FTP server \(NetApp Release (\d+\.\d+\.\d+)([-_a-zA-Z0-9]*)",
        re.IGNORECASE
        )

    tests = {
        "FtpNetApp_1": {
            "global_metadata": {
                "manufacturer": Manufacturer.NETAPP
            },
            "local_metadata": {
                "version": "8.0.5",
                "revision": "P1"
            }
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.manufact_re.search(banner):
            meta.global_metadata.manufacturer = Manufacturer.NETAPP

            version = self.version_re.search(banner).group(1)
            meta.local_metadata.version = version

            rev = self.version_re.search(banner).group(2)
            meta.local_metadata.revision = rev

            return meta
