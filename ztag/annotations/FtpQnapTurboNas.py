import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpQnapTurboNas(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    manufact_re = re.compile("^220 NASFTPD Turbo station", re.IGNORECASE)

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.manufact_re.search(banner):
            meta.global_metadata.device_type = Type.NAS
            meta.global_metadata.manufacturer = Manufacturer.QNAP
            meta.global_metadata.product = "Turbo NAS"

        return meta

    """ Tests
    "220 NASFTPD Turbo station 1.3.2e Server (ProFTPD) [192.168.1.245]\r\n"
    "220 NASFTPD Turbo station 1.3.4e Server (ProFTPD) [192.168.178.5]\r\n"
    "220 NASFTPD Turbo station 1.3.4e Server (ProFTPD) [192.168.70.100]\r\n"
    "220 NASFTPD Turbo station 1.3.4e Server (ProFTPD) [::ffff:192.168.1.99]\r\n"
    "220 NASFTPD Turbo station 2.x 1.3.2e Server (ProFTPD) [192.168.0.2]\r\n"
    "220 NASFTPD Turbo station 1.3.4e Server (ProFTPD) [::ffff:10.100.0.20]\r\n"
    "220 NASFTPD Turbo station 1.3.2e Server (ProFTPD) [192.168.1.38]\r\n"
    "220 NASFTPD Turbo station 1.3.4e Server (ProFTPD) [192.168.1.60]\r\n"
    "220 NASFTPD Turbo station 1.3.4e Server (ProFTPD) [192.168.1.254]\r\n"
    "220 NASFTPD Turbo station 1.3.2e Server (ProFTPD) [192.168.178.103]\r\n"
    "220 NASFTPD Turbo station 1.3.2e Server (ProFTPD) [192.168.178.20]\r\n"
    "220 NASFTPD Turbo station 1.3.4e Server (ProFTPD) [::ffff:192.168.5.10]\r\n"
    "220 NASFTPD Turbo station 1.3.4e Server (ProFTPD) [192.168.1.91]\r\n"
    "220 NASFTPD Turbo station 2.x 1.3.1rc2 Server (ProFTPD) [192.168.3.123]\r\n"
    """
