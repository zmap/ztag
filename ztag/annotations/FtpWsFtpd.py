from ztag.annotation import Annotation
from ztag import protocols
import ztag.test
import re


class IPSwitchFTP(Annotation):
    name = "IPSwitch FTP Server"
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    version_re = re.compile(
        "WS_FTP Server (\d+\.\d+\.\d+)",
        re.IGNORECASE
        )

    def process(self, obj, meta):
        banner = obj["banner"]

        if "ws_ftp server" in banner.lower():
            meta.local_metadata.product = "WS_FTP"
            meta.global_metadata.os = OperatingSystem.WINDOWS
            match = self.version_re.search(banner)
            meta.local_metadata.version = match.group(1)

        return meta

    """ Tests
    "220 aldanmo X2 WS_FTP Server 3.1.3 (2434805489)\r\n"
    "220 ws_ftp X2 WS_FTP Server 7.6.2(48445295)\r\n"
    """
