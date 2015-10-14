import re
from ztag.annotation import Annotation
from ztag import protocols
import ztag.test


class FtpTnFtpd(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    impl_re = re.compile(
        "^220 \d+\.\d+\.\d+\.\d+ FTP server \(tnftpd .+\) ready",
        re.IGNORECASE
        )
    version_re = re.compile("\(tnftpd (.+)\)", re.IGNORECASE)

    tests = {
        "FtpTnFtpd_1": {
            "local_metadata": {
                "product": "tnftpd",
                "version": "20080929"
            }
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.impl_re.search(banner):
            meta.local_metadata.product = "tnftpd"

            version = self.version_re.search(banner).group(1)
            meta.local_metadata.version = version

            return meta

    """ Tests
    "220 192.168.0.3 FTP server (tnftpd 20100324+GSSAPI) ready.\r\n"
    "220 134.91.155.52 FTP server (tnftpd 20100324+GSSAPI) ready.\r\n"
    "220 192.168.1.150 FTP server (tnftpd 20100324+GSSAPI) ready.\r\n"
    "220 172.24.109.49 FTP server (tnftpd 20100324+GSSAPI) ready.\r\n"
    "220 192.168.1.16 FTP server (tnftpd 20100324+GSSAPI) ready.\r\n"
    "220 192.168.44.231 FTP server (tnftpd 20100324+GSSAPI) ready.\r\n"
    "220 88.32.231.138 FTP server (tnftpd 20100324+GSSAPI) ready.\r\n"
    "220 192.168.1.142 FTP server (tnftpd 20100324+GSSAPI) ready.\r\n"
    "220 132.239.167.70 FTP server (tnftpd 20100324+GSSAPI) ready.\r\n"
    "220 192.168.125.8 FTP server (tnftpd 20100324+GSSAPI) ready.\r\n"
    "220 192.168.2.25 FTP server (tnftpd 20100324+GSSAPI) ready.\r\n"
    "220 174.46.174.58 FTP server (tnftpd 20100324+GSSAPI) ready.\r\n"
    "220 192.168.1.3 FTP server (tnftpd 20100324+GSSAPI) ready.\r\n"
    "220 192.168.1.200 FTP server (tnftpd 20100324+GSSAPI) ready.\r\n"
    "220 192.168.10.1 FTP server (tnftpd 20100324+GSSAPI) ready.\r\n"
    "220 184.162.153.21 FTP server (tnftpd 20080929) ready.\r\n"
    "220 192.168.0.9 FTP server (tnftpd 20080929) ready.\r\n"
    "220 10.1.10.50 FTP server (tnftpd 20100324+GSSAPI) ready.\r\n"
    "220 138.87.20.1 FTP server (tnftpd 20100324+GSSAPI) ready.\r\n"
    "220 199.38.81.84 FTP server (tnftpd 20080929) ready.\r\n"
    "220 192.168.2.2 FTP server (tnftpd 20100324+GSSAPI) ready.\r\n"
    "220 192.168.1.11 FTP server (tnftpd 20100324+GSSAPI) ready.\r\n"
    "220 192.168.1.249 FTP server (tnftpd 20100324+GSSAPI) ready.\r\n"
    """
