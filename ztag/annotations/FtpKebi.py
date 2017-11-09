import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag import protocols
import ztag.test


class FtpKebi(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    impl_re = re.compile("^220- Kebi FTP Server", re.IGNORECASE)

    version_re = re.compile("\(Version (\d+(?:\.\d+)*)\)", re.IGNORECASE)


    def process(self, obj, meta):
        banner = obj["banner"]

        if self.impl_re.search(banner):
            meta.local_metadata.product = "Kebi Ftpd"

        match = self.version_re.search(banner)
        if match:
            meta.local_metadata.version = match.group(1)

        return meta

    """ Tests
    "220- Kebi FTP Server ( \\xb1\\xfa\\xba\\xf1 FTP \\xbc\\xad\\xb9\\xf6 )\r\n220- Written by Cho Manik - http://www.webkebi.com\r\n220 Kebi FTP \\xbc\\xad\\xb9\\xf6 \\xc1\\xa2\\xbc\\xd3\\xc0\\xbb \\xc8\\xaf\\xbf\\xb5\\xc7\\xd5\\xb4\\xcf\\xb4\\xd9. !\r\n"
    "220- Kebi FTP Server (Version 2.0.0)\r\n220 Kebi FTP \\xbc\\xad\\xb9\\xf6\\xbf\\xa1 \\xc1\\xa2\\xbc\\xd3\\xc0\\xbb \\xc8\\xaf\\xbf\\xb5\\xc7\\xd5\\xb4\\xcf\\xb4\\xd9. !\r\n"
    "220- Kebi FTP Server (Version 2.0.0)\r\n220 Kebi FTP \\xbc\\xad\\xb9\\xf6\\xbf\\xa1 \\xc1\\xa2\\xbc\\xd3\\xc0\\xbb \\xc8\\xaf\\xbf\\xb5\\xc7\\xd5\\xb4\\xcf\\xb4\\xd9. !\r\n"
    "220- Kebi FTP Server (Version 2.0.0)\r\n220 Kebi FTP \\xbc\\xad\\xb9\\xf6\\xbf\\xa1 \\xc1\\xa2\\xbc\\xd3\\xc0\\xbb \\xc8\\xaf\\xbf\\xb5\\xc7\\xd5\\xb4\\xcf\\xb4\\xd9. !\r\n"
    "220- Kebi FTP Server (Version 2.0.0)\r\n220 SINN \\xbc\\xad\\xb9\\xf6\\xbf\\xa1 \\xc1\\xa2\\xbc\\xd3\\xc0\\xbb \\xc8\\xaf\\xbf\\xb5\\xc7\\xd5\\xb4\\xcf\\xb4\\xd9. !\r\n"
    "220- Kebi FTP Server ( \\xb1\\xfa\\xba\\xf1 FTP \\xbc\\xad\\xb9\\xf6 )\r\n220- Written by Cho Manik - http://www.webkebi.com\r\n220 Easy FTP\r\n"
    "220- Kebi FTP Server ( \\xb1\\xfa\\xba\\xf1 FTP \\xbc\\xad\\xb9\\xf6 )\r\n220- Written by Cho Manik - http://www.webkebi.com\r\n220 Kebi FTP \\xbc\\xad\\xb9\\xf6 \\xc1\\xa2\\xbc\\xd3\\xc0\\xbb \\xc8\\xaf\\xbf\\xb5\\xc7\\xd5\\xb4\\xcf\\xb4\\xd9. !\r\n"
    "220- Kebi FTP Server ( \\xb1\\xfa\\xba\\xf1 FTP \\xbc\\xad\\xb9\\xf6 )\r\n220- Written by Cho Manik - http://www.webkebi.com\r\n220 Kebi FTP \\xbc\\xad\\xb9\\xf6\\xbf\\xa1 \\xc1\\xa2\\xbc\\xd3\\xc0\\xbb \\xc8\\xaf\\xbf\\xb5\\xc7\\xd5\\xb4\\xcf\\xb4\\xd9. !\r\n"
    "220- Kebi FTP Server ( \\xb1\\xfa\\xba\\xf1 FTP \\xbc\\xad\\xb9\\xf6 )\r\n220- Written by Cho Manik - http://www.webkebi.com\r\n220 Kebi FTP \\xbc\\xad\\xb9\\xf6 \\xc1\\xa2\\xbc\\xd3\\xc0\\xbb \\xc8\\xaf\\xbf\\xb5\\xc7\\xd5\\xb4\\xcf\\xb4\\xd9. !\r\n"
    "220- Kebi FTP Server (Version 2.0.0)\r\n220 Kebi FTP \\xbc\\xad\\xb9\\xf6\\xbf\\xa1 \\xc1\\xa2\\xbc\\xd3\\xc0\\xbb \\xc8\\xaf\\xbf\\xb5\\xc7\\xd5\\xb4\\xcf\\xb4\\xd9. !\r\n"
    "220- Kebi FTP Server (Version 2.0.0)\r\n220 Kebi FTP \\xbc\\xad\\xb9\\xf6\\xbf\\xa1 \\xc1\\xa2\\xbc\\xd3\\xc0\\xbb \\xc8\\xaf\\xbf\\xb5\\xc7\\xd5\\xb4\\xcf\\xb4\\xd9. !\r\n"
    "220- Kebi FTP Server (Version 2.0.0)\r\n220 Kebi FTP \\xbc\\xad\\xb9\\xf6\\xbf\\xa1 \\xc1\\xa2\\xbc\\xd3\\xc0\\xbb \\xc8\\xaf\\xbf\\xb5\\xc7\\xd5\\xb4\\xcf\\xb4\\xd9. !\r\n"
    "220- Kebi FTP Server ( \\xb1\\xfa\\xba\\xf1 FTP \\xbc\\xad\\xb9\\xf6 )\r\n220- Written by Cho Manik - http://www.webkebi.com\r\n220 Kebi FTP \\xbc\\xad\\xb9\\xf6\\xbf\\xa1 \\xc1\\xa2\\xbc\\xd3\\xc0\\xbb \\xc8\\xaf\\xbf\\xb5\\xc7\\xd5\\xb4\\xcf\\xb4\\xd9. !\r\n"
    "220- Kebi FTP Server ( \\xb1\\xfa\\xba\\xf1 FTP \\xbc\\xad\\xb9\\xf6 )\r\n220- Written by Cho Manik - http://www.webkebi.com\r\n220 Kebi FTP \\xbc\\xad\\xb9\\xf6 \\xc1\\xa2\\xbc\\xd3\\xc0\\xbb \\xc8\\xaf\\xbf\\xb5\\xc7\\xd5\\xb4\\xcf\\xb4\\xd9. !\r\n"
    """
