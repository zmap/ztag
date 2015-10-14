import re
from ztag.annotation import Annotation
from ztag import protocols
import ztag.test


class FtpVsFtpd(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    versionStr = "\d+\.\d+(\.\d+)?(([a-z])|(rc\d))?"
    impl_re = re.compile(
        "^220 (\()?vsFTPd (\d+(\.\d+)*)[+]?",
        re.IGNORECASE
        )
    version_re = re.compile("vsFTPd (\d+\.\d+\.\d+)", re.IGNORECASE)
    rev_re = re.compile("\((ext\.(?:\d+))\)", re.IGNORECASE)

    tests = {
        "FtpVsFtpd_1": {
            "local_metadata": {
                "product": "vsftpd",
                "version": "2.3.2"
            }
        },
        "FtpVsFtpd_2": {
            "local_metadata": {
                "product": "vsftpd",
                "version": "3.0.2",
                "revision": "ext.1"
            }
        },
        "FtpVsFtpd_3": {
            "local_metadata": {
                "product": "vsftpd",
            },
            "tags": ["Broken installation"]
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if (
            self.impl_re.search(banner) or
            banner.startswith("220 Welcome to the vsftp daemon")
        ):
            meta.local_metadata.product = "vsftpd"

            version = self.version_re.search(banner)
            if version:
                meta.local_metadata.version = version.group(1)

            rev = self.rev_re.search(banner)
            if rev:
                meta.local_metadata.revision = rev.group(1)

        if (
            banner.startswith("500 OOPS: vsftpd: root is not mounted") or
            banner.startswith("500 OOPS: vsftpd: not found: directory given in") or
            banner.startswith("500 OOPS: vsftpd: cannot locate user specified in") or
            banner.startswith("500 OOPS: vsftpd: both local and anonymous access disabled")
        ):
            meta.local_metadata.product = "vsftpd"
            meta.tags.add("Broken installation")

        return meta

    """ Tests
    "220 (vsFTPd 2.3.2)\r\n"
    "220 (vsFTPd 2.0.7)\r\n"
    "500 OOPS: vsftpd: both local and anonymous access disabled!\r\n"
    "220 (vsFTPd 2.3.2)\r\n"
    "500 OOPS: vsftpd: not found: directory given in 'secure_chroot_dir':/usr/share/empty\r\n"
    "220 (vsFTPd 2.2.2)\r\n"
    "220 vsFTPd 3.0.2+ (ext.1) ready...\r\n"
    "220 (vsFTPd 2.2.2)\r\n"
    "220 (vsFTPd 1.1.3)\r\n"
    "220 (vsFTPd 1.1.3)\r\n"
    "220 (vsFTPd 3.0.2)\r\n"
    "220 (vsFTPd 2.2.2)\r\n"
    "220 (vsFTPd 2.0.5)\r\n"
    "500 OOPS: vsftpd: root is not mounted\r\n"
    "220 (vsFTPd 2.2.2)\r\n"
    "220 (vsFTPd 2.2.2)\r\n"
    "220 (vsFTPd 2.3.2)\r\n"
    "220 (vsFTPd 3.0.2)\r\n"
    "220 (vsFTPd 2.1.0)\r\n"
    "500 OOPS: vsftpd: root is not mounted\r\n"
    "220 (vsFTPd 3.0.2)\r\n"
    "220 (vsFTPd 2.0.7)\r\n"
    "220 (vsFTPd 2.3.4)\r\n"
    "220 (vsFTPd 2.0.5)\r\n"
    "220 vsFTPd 2.0.6+ (ext.1) ready... [charset=UTF8]\r\n"
    "220 (vsFTPd 2.0.5)\r\n"
    "220 (vsFTPd 2.3.2)\r\n"
    "220 vsFTPd 2.0.4+ (ext.3) ready...\r\n"
    "220 (vsFTPd 2.2.2)\r\n"
    """
