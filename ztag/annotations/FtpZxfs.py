import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag import protocols
import ztag.test


class FtpZxfs(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    version_re = re.compile("Server v(\d+\.\d+),", re.IGNORECASE)
    revision_re = re.compile("\((build \d+)\)", re.IGNORECASE)

    def process(self, obj, meta):
        banner = obj["banner"]

        if banner.startswith("220-ZXFS Ftp Server v"):
            meta.local_metadata.product = "ZXFS"
            version = self.version_re.search(banner).group(1)
            meta.local_metadata.version = version

            rev = self.revision_re.search(banner)
            if rev:
                meta.local_metadata.revision = rev.group(1)

        return meta

    """ Tests
    "220-ZXFS Ftp Server v1.0, Service ready for new user.\r\n 1 user online, your ip is 141.212.122.224:37454\r\n220 this server supports SIZE, resume broken downloads\r\n"
    "220-ZXFS Ftp Server v1.0, Service ready for new user.\r\n 1 user online, your ip is 141.212.122.224:51903\r\n220 this server supports SIZE, resume broken downloads\r\n"
    "220-ZXFS Ftp Server v1.0, Service ready for new user.\r\n 1 user online, your ip is 141.212.122.224:31863\r\n220 this server supports SIZE, resume broken downloads\r\n"
    "220-ZXFS Ftp Server v1.0, Service ready for new user.\r\n 1 user online, your ip is 141.212.122.224:41810\r\n220 this server supports SIZE, resume broken downloads\r\n"
    "220-ZXFS Ftp Server v1.0(build 1027), Service ready for new user.\r\n 1 user online, your ip is 141.212.122.224:32338\r\n220 this server supports SIZE, resume broken downloads\r\n"
    """
