import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpZyXel(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    manufact_re = re.compile(
        "^220 P(-)?660[HDR].* FTP version 1\.0 ready at",
        re.IGNORECASE
        )
    product_re = re.compile(
        "^220 (.+) FTP version",
        re.IGNORECASE
        )

    tests = {
        "FtpZyXel_1": {
            "global_metadata": {
                "device_type": Type.DSL_MODEM,
                "manufacturer": Manufacturer.ZYXEL,
                "product": "P-660RU-T1v2"
            }
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.manufact_re.search(banner):
            meta.global_metadata.device_type = Type.DSL_MODEM
            meta.global_metadata.manufacturer = Manufacturer.ZYXEL

            product = self.product_re.search(banner).group(1)
            meta.global_metadata.product = product

            return meta

    """ Tests
    "220 P-660HW-T FTP version 1.0 ready at Mon Jun 22 02:31:19 2015\r\n"
    "220 P-660R-D1 FTP version 1.0 ready at Mon Jun 22 01:30:16 2015\r\n"
    "220 P-660RU-T FTP version 1.0 ready at Tue May 02 00:42:54 2000\r\n"
    "220 P660RU-T1 FTP version 1.0 ready at Mon Oct 21 17:57:13 2002\r\n"
    "220 P-660R-T1v2 FTP version 1.0 ready at Tue Jan 04 09:52:52 2000\r\n"
    "220 P660RU-T1 FTP version 1.0 ready at Sat Dec 08 21:20:29 2001\r\n"
    "220 P-660R-T1v2 FTP version 1.0 ready at Thu Jan 06 22:16:02 2000\r\n"
    "220 P-660H-T1 FTP version 1.0 ready at Thu Mar 02 21:48:47 2000\r\n"
    "220 P-660RU-T1v2 FTP version 1.0 ready at Tue Jan 25 05:02:34 2000\r\n"
    "220 P660RU-T1 FTP version 1.0 ready at Sat Feb 05 23:55:32 2000\r\n"
    "220 P-660H-T1 FTP version 1.0 ready at Sun Jan 02 17:32:08 2000\r\n"
    "220 P-660HW-T FTP version 1.0 ready at Sat Apr 22 15:29:47 2000\r\n"
    "220 P-660H-T1_v2 FTP version 1.0 ready at Fri Sep 08 08:40:22 2000\r\n"
    "220 P660RU-T1 FTP version 1.0 ready at Thu Jul 06 13:53:18 2000\r\n"
    "220 P-660RU-T3v2 FTP version 1.0 ready at Tue Feb 15 03:07:40 2000\r\n"
    "220 P660RU-T3 FTP version 1.0 ready at Fri Sep 01 23:43:42 2000\r\n"
    "220 P-660HW-T FTP version 1.0 ready at Mon Jul 09 06:22:06 2001\r\n"
    "220 P-660HW-T FTP version 1.0 ready at Mon Jan 17 01:54:28 2000\r\n"
    "220 P-660RU-T1v2 FTP version 1.0 ready at Thu Mar 09 20:28:31 2000\r\n"
    "220 P-660R-T1v2 FTP version 1.0 ready at Tue Jan 11 06:02:29 2000\r\n"
    "220 P-660RU-T1v2 FTP version 1.0 ready at Tue Jan 04 06:59:11 2000\r\n"
    "220 P-660R-T1v2 FTP version 1.0 ready at Sat Jan 01 04:23:12 2000\r\n"
    """
