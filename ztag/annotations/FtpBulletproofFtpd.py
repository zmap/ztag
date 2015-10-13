import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag import protocols
import ztag.test


class FtpBulletproofFtpd(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    impl_re = re.compile("^220[- ]BulletProof FTP Server ready", re.IGNORECASE)

    def process(self, obj, meta):
        banner = obj["banner"]
        if self.impl_re.search(banner):
            meta.global_metadata.os = OperatingSystem.WINDOWS
            meta.local_metadata.product = "BulletProof FTP"

        return meta

    """ Tests
    "220 BulletProof FTP Server ready ...\r\n"
    "220 BulletProof FTP Server ready ...\r\n"
    "220 BulletProof FTP Server ready ...\r\n"
    "220 BulletProof FTP Server ready ...\r\n"
    "220 BulletProof FTP Server ready ...\r\n"
    "220 BulletProof FTP Server ready ...\r\n"
    "220 BulletProof FTP Server ready ...\r\n"
    "220 BulletProof FTP Server ready ...\r\n"
    "220 BulletProof FTP Server ready ...\r\n"
    "220 BulletProof FTP Server ready ...\r\n"
    "220 BulletProof FTP Server ready ...\r\n"
    "220 BulletProof FTP Server ready ...\r\n"
    "220 BulletProof FTP Server ready ...\r\n"
    "220 BulletProof FTP Server ready ...\r\n"
    "220 BulletProof FTP Server ready ...\r\n"
    "220 BulletProof FTP Server ready ...\r\n"
    """
