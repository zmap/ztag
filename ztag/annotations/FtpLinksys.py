import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpLinksys(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    manufact_re = re.compile("^220 Welcome to linksys", re.IGNORECASE)

    version_re = re.compile(
        "ProFTPD (\d+\.\d+\.\d+)(rc\d+) Server",
        re.IGNORECASE
        )

    tests = {
        "FtpLinksys_1": {
            "global_metadata": {
                "manufacturer": Manufacturer.LINKSYS
            }
        },
        "FtpLinksys_2": {
            "global_metadata": {
                "manufacturer": Manufacturer.LINKSYS,
                "product": "WRT350N"
            },
            "local_metadata": {
                "product": "ProFTPD",
                "version": "1.3.0",
                "revision": "rc2"
            }
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.manufact_re.search(banner):
            meta.global_metadata.manufacturer = Manufacturer.LINKSYS

        if "(LinksysWRT350N)" in banner:
            meta.global_metadata.manufacturer = Manufacturer.LINKSYS
            meta.global_metadata.product = "WRT350N"

            match = self.version_re.search(banner)
            if match:
                meta.local_metadata.product = "ProFTPD"
                meta.local_metadata.version = match.group(1)
                meta.local_metadata.revision = match.group(2)

        return meta

    """ Tests
    "220 Welcome to Linksys-EA6500\r\n"
    "220 Welcome to Linksys16746\r\n"
    "220 Welcome to Linksys01332\r\n"
    "220 Welcome to linksys-E3000's FTP service\r\n"
    "220 Welcome to Linksys02804\r\n"
    "220 Welcome to Linksys00954\r\n"
    "220 Welcome to Linksys28853\r\n"
    "220 Welcome to Linksys02905\r\n"
    "220 Welcome to LinksysDUBURT19\r\n"
    "220 Welcome to Linksys06088\r\n"
    "220 Welcome to Linksys37850\r\n"
    "220 Welcome to LinksysTB\r\n"
    "220 Welcome to Linksys07607\r\n"
    "220 Welcome to Linksys09695\r\n"
    "220 Welcome to Linksys12796\r\n"
    "220 Welcome to Linksys24327\r\n"
    "220 Welcome to Linksys00593\r\n"
    "220 Welcome to Linksys08333\r\n"
    "220 Welcome to Linksys01242\r\n"
    "220 Welcome to Linksys02893\r\n"
    "220 Welcome to Linksys03761\r\n"
    "220 Welcome to Linksys15480\r\n"
    "220 ProFTPD 1.3.0rc2 Server (LinksysWRT350N) [75.108.213.142]\r\n"
    "220 ProFTPD 1.3.0rc2 Server (LinksysWRT350N) [186.188.101.45]\r\n"
    "220 ProFTPD 1.3.0rc2 Server (LinksysWRT350N) [70.187.168.41]\r\n"
    "220 ProFTPD 1.3.0rc2 Server (LinksysWRT350N) [66.41.202.76]\r\n"
    "220 ProFTPD 1.3.0rc2 Server (LinksysWRT350N) [68.199.51.173]\r\n"
    "220 ProFTPD 1.3.0rc2 Server (LinksysWRT350N) [67.193.14.120]\r\n"
    "220 ProFTPD 1.3.0rc2 Server (LinksysWRT350N) [72.193.207.196]\r\n"
    "220 ProFTPD 1.3.0rc2 Server (LinksysWRT350N) [24.44.99.216]\r\n"
    "220 ProFTPD 1.3.0rc2 Server (LinksysWRT350N) [24.87.129.105]\r\n"
    """
