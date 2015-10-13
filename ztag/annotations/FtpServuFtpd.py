import re
from ztag.annotation import Annotation
from ztag import protocols
import ztag.test


class FtpServuFtpd(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    impl_re = re.compile(
        "^220 Serv-U FTP[- ]Server v\d+.\d+[a-z]? (for WinSock )?ready\.",
        re.IGNORECASE
        )
    version_re = re.compile("Server v(\d+\.\d+)", re.IGNORECASE)

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.impl_re.search(banner):
            meta.local_metadata.product = "Serv-U"
            version = self.version_re.search(banner).group(1)
            meta.local_metadata.version = version

            if "WinSock" in banner:
                meta.global_metadata.os = OperatingSystem.WINDOWS

        return meta

    """ Tests
    "220 Serv-U FTP Server v5.0 for WinSock ready...\r\n"
    "220 Serv-U FTP Server v15.0 ready...\r\n"
    "220 Serv-U FTP Server v6.4 for WinSock ready...\r\n"
    "220 Serv-U FTP Server v15.1 ready...\r\n"
    "220 Serv-U FTP Server v9.3 ready...\r\n"
    "220 Serv-U FTP Server v14.0 ready...\r\n"
    "220 Serv-U FTP Server v14.0 ready...\r\n"
    "220 Serv-U FTP Server v6.2 for WinSock ready...\r\n"
    "220 Serv-U FTP Server v6.2 for WinSock ready...\r\n"
    "220 Serv-U FTP Server v6.4 for WinSock ready...\r\n"
    "220 Serv-U FTP Server v6.4 for WinSock ready...\r\n"
    "220 Serv-U FTP Server v6.2 for WinSock ready...\r\n"
    "220 Serv-U FTP Server v6.2 for WinSock ready...\r\n"
    "220 Serv-U FTP Server v6.2 for WinSock ready...\r\n"
    "220 Serv-U FTP Server v6.2 for WinSock ready...\r\n"
    "220 Serv-U FTP Server v6.4 for WinSock ready...\r\n"
    "220 Serv-U FTP Server v6.4 for WinSock ready...\r\n"
    "220 Serv-U FTP Server v6.4 for WinSock ready...\r\n"
    "220 Serv-U FTP Server v6.3 for WinSock ready...\r\n"
    "220 Serv-U FTP Server v6.1 for WinSock ready...\r\n"
    "220 Serv-U FTP-Server v2.5j for WinSock ready...\r\n"
    "220 Serv-U FTP Server v6.3 for WinSock ready...\r\n"
    "220 Serv-U FTP Server v15.0 ready...\r\n"
    "220 Serv-U FTP Server v6.4 for WinSock ready...\r\n"
    "220 Serv-U FTP Server v6.4 for WinSock ready...\r\n"
    """
