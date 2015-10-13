import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpLacie(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    product_re_dict = {
        "2Big": re.compile("^220 LaCie-2big(-NAS)? FTP Server", re.IGNORECASE),
        "5Big": re.compile(
            "^220 LaCie-5big(-NAS)?(-Pro)? FTP Server",
            re.IGNORECASE
            ),
        "D2": re.compile("^220 LaCie-d2 FTP Server", re.IGNORECASE),
        "CloudBox": re.compile(
            "^220 LaCie-CloudBox FTP Server",
            re.IGNORECASE
            ),
        "Network Space 2": re.compile(
            "^220 NetworkSpace2 FTP Server",
            re.IGNORECASE
            ),
        "": re.compile(
            "^220 LaCie(-NAS)? FTP Server \[\d+\.\d+\.\d+\.\d+\]",
            re.IGNORECASE
            ),
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        found = ""
        for product, regex in self.product_re_dict.items():
            if regex.search(banner):
                meta.global_metadata.device_type = Type.NAS
                meta.global_metadata.manufacturer = Manufacturer.LACIE
                found = " && ".join([found, product])

        if found != "":
            meta.global_metadata.product = found

        return meta

    """ Tests
    "220 NetworkSpace2 FTP Server [10.0.1.50]\r\n"
    "220 LaCie-CloudBox FTP Server [192.168.0.16]\r\n"
    "220 LaCie-CloudBox FTP Server [192.168.0.21]\r\n"
    "220 LaCie-CloudBox FTP Server [192.168.1.197]\r\n"
    "220 NetworkSpace2 FTP Server [192.168.100.17]\r\n"
    "220 LaCie-CloudBox FTP Server [192.168.1.11]\r\n"
    "220 NetworkSpace2 FTP Server [192.168.0.26]\r\n"
    "220 LaCie-CloudBox FTP Server [192.168.1.93]\r\n"
    "220 LaCie-2big FTP Server [192.168.1.206]\r\n"
    "220 NetworkSpace2 FTP Server [192.168.0.13]\r\n"
    "220 NetworkSpace2 FTP Server [192.168.0.19]\r\n"
    "220 LaCie-CloudBox FTP Server [192.168.0.100]\r\n"
    "220 LaCie-CloudBox FTP Server [192.168.1.59]\r\n"
    "220 NetworkSpace2 FTP Server [192.168.0.100]\r\n"
    "220 LaCie-CloudBox FTP Server [192.168.1.3]\r\n"
    "220 NetworkSpace2 FTP Server [192.168.1.24]\r\n"
    "220 LaCie-2big FTP Server [192.168.178.31]\r\n"
    "220 LaCie-CloudBox FTP Server [192.168.1.12]\r\n"
    "220 NetworkSpace2 FTP Server [192.168.0.128]\r\n"
    "220 LaCie-5big FTP Server [192.168.0.5]\r\n"
    "220 LaCie-d2 FTP Server [192.168.10.152]\r\n"
    "220 LaCie-5big-Pro FTP Server [::ffff:192.168.1.24]\r\n"
    "220 LaCie-2big-NAS FTP Server [192.168.1.250]\r\n"
    "220 NetworkSpace2 FTP Server [192.168.0.103]\r\n"
    "220 NetworkSpace2 FTP Server [192.168.1.39]\r\n"
    "220 LaCie FTP Server [192.168.1.34]\r\n"
    """
