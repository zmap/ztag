import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpZte(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    manufact_re = re.compile(
        "^220 OX253P FTP version 1.0 ready at",
        re.IGNORECASE
        )

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.manufact_re.search(banner):
            meta.global_metadata.device_type = Type.INFRASTRUCTURE_ROUTER
            meta.global_metadata.manufacturer = Manufacturer.ZTE
            meta.global_metadata.manufacturer = "OX253P"

        return meta

    """ Tests
    "220 OX253P FTP version 1.0 ready at Mon Dec 27 09:06:04 2010\r\n"
    "220 OX253P FTP version 1.0 ready at Thu Aug 14 07:32:27 2014\r\n"
    "220 OX253P FTP version 1.0 ready at Wed Dec 22 17:08:49 2010\r\n"
    "220 OX253P FTP version 1.0 ready at Mon Jun 22 05:01:03 2015\r\n"
    "220 OX253P FTP version 1.0 ready at Mon Jun 22 05:01:16 2015\r\n"
    "220 OX253P FTP version 1.0 ready at Mon Jun 22 05:01:52 2015\r\n"
    "220 OX253P FTP version 1.0 ready at Mon Jun 22 05:01:54 2015\r\n"
    "220 OX253P FTP version 1.0 ready at Mon Jun 22 05:01:57 2015\r\n"
    "220 OX253P FTP version 1.0 ready at Mon May 06 08:00:58 2013\r\n"
    "220 OX253P FTP version 1.0 ready at Mon Jun 22 05:02:08 2015\r\n"
    "220 OX253P FTP version 1.0 ready at Mon Jun 22 05:02:17 2015\r\n"
    "220 OX253P FTP version 1.0 ready at Mon Jun 22 05:02:18 2015\r\n"
    "220 OX253P FTP version 1.0 ready at Mon Jun 22 05:02:25 2015\r\n"
    "220 OX253P FTP version 1.0 ready at Wed Dec 22 10:54:59 2010\r\n"
    "220 OX253P FTP version 1.0 ready at Mon Jun 22 05:02:22 2015\r\n"
    "220 OX253P FTP version 1.0 ready at Mon Jun 22 05:02:41 2015\r\n"
    "220 OX253P FTP version 1.0 ready at Wed Dec 22 13:28:28 2010\r\n"
    "220 OX253P FTP version 1.0 ready at Wed Dec 22 05:48:21 2010\r\n"
    "220 OX253P FTP version 1.0 ready at Mon Jun 22 05:03:03 2015\r\n"
    "220 OX253P FTP version 1.0 ready at Mon Jun 22 05:03:04 2015\r\n"
    "220 OX253P FTP version 1.0 ready at Mon Jun 22 05:03:10 2015\r\n"
    "220 OX253P FTP version 1.0 ready at Mon Jun 22 05:03:11 2015\r\n"
    """
