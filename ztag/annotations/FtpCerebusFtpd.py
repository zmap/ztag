import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag import protocols
import ztag.test


class FtpCerebusFtpd(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    impl_re = re.compile(
        "^220-(Welcome to )?Cerberus FTP Server",
        re.IGNORECASE
        )

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.impl_re.search(banner):
            meta.global_metadata.os = OperatingSystem.WINDOWS
            meta.local_metadata.product = "Cerberus FTPd"
            if "Personal Edition" in banner:
                meta.local_metadata.version = "Personal"
            elif "Home Edition" in banner:
                meta.local_metadata.version = "Home"

        return meta

    """ Tests
    "220-Cerberus FTP Server - Personal Edition\r\n220-UNREGISTERED\r\n220-Welcome to KeSha Enterprises FTP Server\r\n220 Created by Cerberus, LLC\r\n"
    "220-Cerberus FTP Server - Home Edition\r\n220-This is the UNLICENSED Home Edition and may be used for home, personal use only\r\n220-Welcome to Cerberus FTP Server\r\n220 Created by Cerberus, LLC\r\n"
    "220-Cerberus FTP Server - Personal Edition\r\n220-UNREGISTERED\r\n220-Welcome to Cerberus FTP Server\r\n220 Created by Cerberus, LLC\r\n"
    "220-Welcome to Cerberus FTP Server\r\n220 Created by Cerberus, LLC\r\n"
    "220-Cerberus FTP Server - Home Edition\r\n220-This is the UNLICENSED Home Edition and may be used for home, personal use only\r\n220-Welcome to Cerberus FTP Server\r\n220 Created by Cerberus, LLC\r\n"
    "220-Cerberus FTP Server Personal Edition\r\n220-UNREGISTERED\r\n220-Welcome to Cerberus FTP Server\r\n220 \r\n"
    "220-Welcome to Cerberus FTP Server\r\n220 Created by Cerberus, LLC\r\n"
    "220-Cerberus FTP Server - Personal Edition\r\n220-UNREGISTERED\r\n220 ftp.mrcdescollines.com\r\n"
    "220-Cerberus FTP Server - Home Edition\r\n220-This is the UNLICENSED Home Edition and may be used for home, personal use only\r\n220 \r\n"
    "220-Cerberus FTP Server - Home Edition\r\n220-This is the UNLICENSED Home Edition and may be used for home, personal use only\r\n220-Welcome to Cerberus FTP Server\r\n220 Created by Cerberus, LLC\r\n"
    "220-Cerberus FTP Server - Home Edition\r\n220-This is the UNLICENSED Home Edition and may be used for home, personal use only\r\n220-Welcome to Cerberus FTP Server\r\n220 Created by Cerberus, LLC\r\n"
    "220-Cerberus FTP Server - Personal Edition\r\n220-UNREGISTERED\r\n220 Welcome to the P13 FTP Site\r\n"
    "220-Cerberus FTP Server - Home Edition\r\n220-This is the UNLICENSED Home Edition and may be used for home, personal use only\r\n220-Welcome to Cerberus FTP Server\r\n220 Created by Cerberus, LLC\r\n"
    """
