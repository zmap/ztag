import re
from ztag.annotation import Annotation
from ztag import protocols
import ztag.test


class FtpProFtpd(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    tests = {
        "FtpProFtpd_1": {
            "local_metadata": {
                "product": "ProFTPD",
                "version": "1.3.1",
            }
        },
        "FtpProFtpd_2": {
            "local_metadata": {
                "product": "ProFTPD",
                "version": "1.3.4",
                "revision": "a"
            }
        }
    }

    version_re = re.compile(
        "ProFTPD (\d+\.\d+\.\d+)([a-z])? Server",
        re.IGNORECASE
        )

    def process(self, obj, meta):
        banner = obj["banner"]

        if banner.startswith("220 ProFTPD"):
            meta.local_metadata.product = "ProFTPD"

            version = self.version_re.search(banner).group(1)
            meta.local_metadata.version = version

            rev = self.version_re.search(banner).group(2)
            meta.local_metadata.revision = rev

        return meta

    """ Tests
    "220 ProFTPD 1.3.1 Server (Karl der Grosse) [::ffff:78.46.95.51]\r\n"
    "220 ProFTPD 1.3.1 Server ready.\r\n"
    "220 ProFTPD 1.3.4a Server (Debian) [::ffff:172.24.3.5]\r\n"
    "220 ProFTPD 1.3.3g Server (Main FTP Server) [173.83.162.196]\r\n"
    "220 ProFTPD 1.3.3g Server (Main FTP Server) [76.162.48.228]\r\n"
    "220 ProFTPD 1.3.3g Server (ns17.ixwebhosting.com -> 98.130.253.162) [96.0.153.54]\r\n"
    "220 ProFTPD 1.3.3g Server (tuvitrina.es) [66.116.215.88]\r\n"
    "220 ProFTPD 1.3.0 Server (webhost.sover.net) [216.114.156.36]\r\n"
    "220 ProFTPD 1.3.3g Server (Zpanel FTP Server) [::ffff:10.0.0.45]\r\n"
    "220 ProFTPD 1.3.1 Server (ProFTPD) [125.6.135.156]\r\n"
    "220 ProFTPD 1.3.5 Server (ProFTPD) [64.207.176.121]\r\n"
    "220 ProFTPD 1.3.4a Server (ProFTPD) [69.43.195.179]\r\n"
    "220 ProFTPD 1.3.4a Server (SRV-LNX-06) [192.168.39.79]\r\n"
    "220 ProFTPD 1.3.5 Server (MyArena.ru) [::ffff:46.174.54.243]\r\n"
    "220 ProFTPD 1.3.3c Server (ProFTPD) [64.6.248.40]\r\n"
    "220 ProFTPD 1.3.3 Server (ProFTPD excelsior.thenetnow.com Daemon) [207.112.4.36]\r\n"
    "220 ProFTPD 1.3.3g Server (Main FTP Server) [98.130.207.182]\r\n"
    "220 ProFTPD 1.3.3g Server (Main FTP Server) [71.18.219.49]\r\n"
    "220 ProFTPD 1.3.3g Server (Main FTP Server) [74.91.184.38]\r\n"
    "220 ProFTPD 1.3.3g Server (Main FTP Server) [173.83.75.62]\r\n"
    """
