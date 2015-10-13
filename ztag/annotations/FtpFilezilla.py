import re
from ztag.annotation import Annotation
from ztag import protocols
import ztag.test


class FtpFilezilla(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    product_re = re.compile("^220[- ]FileZilla Server", re.IGNORECASE)
    version_re = re.compile(
        "^220[- ]FileZilla Server( version)? (v)?(\d+\.\d+\.\d+)",
        re.IGNORECASE
        )

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.product_re.search(banner):
            meta.local_metadata.product = "FileZilla"
            version = self.version_re.search(banner)
            if version:
                meta.local_metadata.version = version.group(3)

        return meta

    """ Tests
    "220-FileZilla Server version 0.9.43 beta\r\n220-written by Tim Kosse (tim.kosse@filezilla-project.org)\r\n220 Please visit http://sourceforge.net/projects/filezilla/\r\n"
    "220-FileZilla Server version 0.9.43 beta\r\n220-written by Tim Kosse (tim.kosse@filezilla-project.org)\r\n220 Please visit http://sourceforge.net/projects/filezilla/\r\n"
    "220 FileZilla Server version 0.9.41 beta\r\n"
    "220-FileZilla Server 0.9.51 beta\r\n220-written by Tim Kosse (tim.kosse@filezilla-project.org)\r\n220 Please visit https://filezilla-project.org/\r\n"
    "220-FileZilla Server version 0.9.48 beta\r\n220-written by Tim Kosse (tim.kosse@filezilla-project.org)\r\n220 Please visit https://filezilla-project.org/\r\n"
    "220-FileZilla Server version 0.9.23 beta\r\n220-written by Tim Kosse (Tim.Kosse@gmx.de)\r\n220 Please visit http://sourceforge.net/projects/filezilla/\r\n"
    "220-FileZilla Server v0.9.30 beta\r\n220-written by Tim Kosse (Tim.Kosse@gmx.de)\r\n220 Please visit http://sourceforge.net/projects/filezilla/\r\n"
    "220-FileZilla Server version 0.9.41 beta\r\n220-written by Tim Kosse (Tim.Kosse@gmx.de)\r\n220 Please visit http://sourceforge.net/projects/filezilla/\r\n"
    "220-FileZilla Server version 0.9.41 beta\r\n220-written by Tim Kosse (Tim.Kosse@gmx.de)\r\n220 Please visit http://sourceforge.net/projects/filezilla/\r\n"
    "220-FileZilla Server version 0.9.29 beta\r\n220 HBINGHAMGROUP\r\n"
    "220-FileZilla Server version 0.9.48 beta\r\n220-written by Tim Kosse (tim.kosse@filezilla-project.org)\r\n220 Please visit https://filezilla-project.org/\r\n"
    "220-FileZilla Server version 0.9.34 beta\r\n220-written by Tim Kosse (Tim.Kosse@gmx.de)\r\n220 Please visit http://sourceforge.net/projects/filezilla/\r\n"
    "220-FileZilla Server version 0.9.31 beta\r\n220-written by Tim Kosse (Tim.Kosse@gmx.de)\r\n220 Please visit http://sourceforge.net/projects/filezilla/\r\n"
    "220 FileZilla Server version 0.9.34 beta written by Tim Kosse (Tim.Kosse@gmx.de) Please visit http://sourceforge.\r\n"
    "220-FileZilla Server version 0.9.42 beta\r\n220-written by Tim Kosse (tim.kosse@filezilla-project.org)\r\n220 Please visit http://sourceforge.net/projects/filezilla/\r\n"
    "220-FileZilla Server version 0.9.49 beta\r\n220-written by Tim Kosse (tim.kosse@filezilla-project.org)\r\n220 Please visit https://filezilla-project.org/\r\n"
    "220 FileZilla Server version 0.9.49 beta written by Tim Kosse (Tim.Kosse@gmx.de) Please visit http://sourceforge.\r\n"
    "220 FileZilla Server version 0.9.36 beta written by Tim Kosse (Tim.Kosse@gmx.de) Please visit http://sourceforge.\r\n"
    "220-FileZilla Server version 0.9.46 beta\r\n220-written by Tim Kosse (tim.kosse@filezilla-project.org)\r\n220 Please visit http://sourceforge.net/projects/filezilla/\r\n"
    "220-FileZilla Server version 0.9.24 beta\r\n220-written by Tim Kosse (Tim.Kosse@gmx.de)\r\n220 Please visit http://sourceforge.net/projects/filezilla/\r\n"
    """
