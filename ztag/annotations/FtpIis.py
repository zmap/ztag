import re
from ztag.annotation import Annotation
from ztag import protocols
import ztag.test


class FtpIis(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    manufacturer_re = re.compile(
        "^220[- ]Microsoft FTP Service",
        re.IGNORECASE
        )

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.manufacturer_re.search(banner):
            meta.global_metadata.os = OperatingSystem.WINDOWS
            meta.local_metadata.product = "IIS"

        return meta

    """ Tests
    "220 Microsoft FTP Service\r\n"
    "220 Microsoft FTP Service\r\n"
    "220-Microsoft FTP Service\r\n220 \\xbb\\xb6\\xd3\\xad\\xc4\\xfa\\xca\\xb9\\xd3\\xc3\\xcd\\xf2\\xcd\\xf8\\xd6\\xf7\\xbb\\xfa\\xa3\\xac\\xc8\\xe7\\xb9\\xfb\\xc4\\xfaFTP\\xb5\\xc7\\xc2\\xbd\\xd5\\xcb\\xbb\\xa7\\xd1\\xe9\\xd6\\xa4\\xca\\xa7\\xb0\\xdc\\xa3\\xac\\xc7\\xeb\\xb5\\xc7\\xc2\\xbd\\xd6\\xf7\\xbb\\xfa\\xbf\\xd8\\xd6\\xc6\\xc3\\xe6\\xb0\\xe5\\xa3\\xbacp.hichina.com\\xbd\\xf8\\xd0\\xd0\\xbf\\xda\\xc1\\xee\\xd6\\xd8\\xd6\\xc3\r\n"
    "220 Microsoft FTP Service\r\n"
    "220-Microsoft FTP Service\r\n220 \\xbb\\xb6\\xd3\\xad\\xc4\\xfa\\xca\\xb9\\xd3\\xc3\\xcd\\xf2\\xcd\\xf8\\xd6\\xf7\\xbb\\xfa\\xa3\\xac\\xc8\\xe7\\xb9\\xfb\\xc4\\xfaFTP\\xb5\\xc7\\xc2\\xbd\\xd5\\xcb\\xbb\\xa7\\xd1\\xe9\\xd6\\xa4\\xca\\xa7\\xb0\\xdc\\xa3\\xac\\xc7\\xeb\\xb5\\xc7\\xc2\\xbd\\xd6\\xf7\\xbb\\xfa\\xbf\\xd8\\xd6\\xc6\\xc3\\xe6\\xb0\\xe5\\xa3\\xbacp.hichina.com\\xbd\\xf8\\xd0\\xd0\\xbf\\xda\\xc1\\xee\\xd6\\xd8\\xd6\\xc3\r\n"
    "220 Microsoft FTP Service\r\n"
    "220 Microsoft FTP Service\r\n"
    "220 Microsoft FTP Service\r\n"
    """
