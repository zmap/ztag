import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpIpTime(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    manufact_re = re.compile("^220 ipTIME_FTPD", re.IGNORECASE)
    version_re = re.compile(
        "^220 ipTIME_FTPD (\d+\.\d+\.\d+[a-z]) Server",
        re.IGNORECASE
        )

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.manufact_re.search(banner):
            meta.global_metadata.manufacturer = Manufacturer.IPTIME
            version = self.version_re.search(banner).group(1)
            meta.local_metadata.version = version

        return meta

    """ Tests
    "220 ipTIME_FTPD 1.3.4d Server (SCJY0207-1B34D2) [114.204.150.130]\r\n"
    "220 ipTIME_FTPD 1.3.4d Server (salesteam-1B269F) [1.236.244.185]\r\n"
    "220 ipTIME_FTPD 1.3.4d Server (NAS2-AB1769) [192.168.219.173]\r\n"
    "220 ipTIME_FTPD 1.3.4d Server (NAS2-C93E2D) [192.168.0.8]\r\n"
    "220 ipTIME_FTPD 1.3.4d Server (youilind-AB11EE) [192.168.0.126]\r\n"
    "220 ipTIME_FTPD 1.3.0 Server (NAS2-C9219D) [192.168.0.100]\r\n"
    "220 ipTIME_FTPD 1.3.4d Server (ipTIME A5004NS-653987) [::ffff:192.168.0.1]\r\n"
    "220 ipTIME_FTPD 1.3.4d Server (ZEMNASII-C93575) [192.168.0.200]\r\n"
    "220 ipTIME_FTPD 1.3.4d Server (hiliving-AB01BF) [192.168.0.2]\r\n"
    "220 ipTIME_FTPD 1.3.4d Server (ipTIME A2004NS-1085D9) [192.168.0.1]\r\n"
    "220 ipTIME_FTPD 1.3.4d Server (SKFOOD-C92AB6) [192.168.11.200]\r\n"
    "220 ipTIME_FTPD 1.3.0 Server (NAS2-C93479) [192.168.0.18]\r\n"
    "220 ipTIME_FTPD 1.3.4d Server (ipTIME A3004NS-DA1841) [::ffff:192.168.0.1]\r\n"
    """
