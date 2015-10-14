import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpTenor(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    manufact_re = re.compile(
        "Tenor Multipath Switch FTP Server",
        re.IGNORECASE
        )
    version_re = re.compile(
        "FTP server \(Version ([a-zA-Z]+)(?: )?(\d+\.\d+\.\d+)\)",
        re.IGNORECASE
        )
    
    tests = {
        "FtpTenor_1": {
            "global_metadata": {
                "device_type": Type.SOHO_ROUTER,
                "manufacturer": Manufacturer.SONUS,
                "product": "Tenor Multipath Switch",
            },
            "local_metadata": {
                "product": "VxWorks",
                "version": "5.4.2"
            }
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.manufact_re.search(banner):
            meta.global_metadata.device_type = Type.SOHO_ROUTER
            meta.global_metadata.manufacturer = Manufacturer.SONUS
            meta.global_metadata.product = "Tenor Multipath Switch"

            match = self.version_re.search(banner)
            meta.local_metadata.product = match.group(1)
            meta.local_metadata.version = match.group(2)

        return meta

    """ Tests
    "220 <2056728e>  Tenor Multipath Switch FTP server (Version VxWorks5.4.2) ready.\r\n"
    "220 <5882a65a>  Tenor Multipath Switch FTP server (Version VxWorks5.4.2) ready.\r\n"
    "220 <556541bd>  Tenor Multipath Switch FTP server (Version VxWorks5.4.2) ready.\r\n"
    "220 <d89fbb47>  Tenor Multipath Switch FTP server (Version VxWorks5.4.2) ready.\r\n"
    "220 <623115e9>  Tenor Multipath Switch FTP server (Version VxWorks5.4.2) ready.\r\n"
    "220 <3582a65a>  Tenor Multipath Switch FTP server (Version VxWorks5.4.2) ready.\r\n"
    "220 <f3d5f10d>  Tenor Multipath Switch FTP server (Version VxWorks5.4.2) ready.\r\n"
    "220 <8287a35f>  Tenor Multipath Switch FTP server (Version VxWorks5.4.2) ready.\r\n"
    "220 <5ab6926e>  Tenor Multipath Switch FTP server (Version VxWorks5.4.2) ready.\r\n"
    "220 <a2b6926e>  Tenor Multipath Switch FTP server (Version VxWorks5.4.2) ready.\r\n"
    "220 <83a5817d>  Tenor Multipath Switch FTP server (Version VxWorks5.4.2) ready.\r\n"
    "220 <7fac8874>  Tenor Multipath Switch FTP server (Version VxWorks5.4.2) ready.\r\n"
    "220 <35bb9f63>  Tenor Multipath Switch FTP server (Version VxWorks5.4.2) ready.\r\n"
    "220 <45cbef13>  Tenor Multipath Switch FTP server (Version VxWorks5.4.2) ready.\r\n"
    "220 <d60125d9>  Tenor Multipath Switch FTP server (Version VxWorks5.4.2) ready.\r\n"
    "220 <aedafe02>  Tenor Multipath Switch FTP server (Version VxWorks5.4.2) ready.\r\n"
    "220 <b984a05c>  Tenor Multipath Switch FTP server (Version VxWorks5.4.2) ready.\r\n"
    "220 <f37753af>  Tenor Multipath Switch FTP server (Version VxWorks5.4.2) ready.\r\n"
    """
