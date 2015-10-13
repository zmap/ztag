import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpSharp(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    manufact_re = re.compile(
        "^220 SHARP ((MX)|(AR))-[0-9A-Z]+ Ver \d+(\.[0-9a-z]+)+ FTP server",
        re.IGNORECASE
        )
    product_re = re.compile("SHARP (.+) Ver", re.IGNORECASE)
    version_re = re.compile(
        "Ver (\d+(\.\d+)*)([a-z])? FTP",
        re.IGNORECASE
        )

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.manufact_re.search(banner):
            meta.global_metadata.device_type = Type.GENERIC_PRINTER
            meta.global_metadata.manufacturer = Manufacturer.SHARP

            product = self.product_re.search(banner).group(1)
            meta.global_metadata.product = product

            version = self.version_re.search(banner).group(1)
            rev = self.version_re.search(banner).group(3)
            meta.local_metadata.version = version
            meta.local_metadata.revision = rev

        return meta

    """ Tests
    "220 SHARP MX-3100N Ver 01.05.00.0b FTP server.\r\n"
    "220 SHARP MX-2010U Ver 01.05.00.2k.56 FTP server.\r\n"
    "220 SHARP MX-2300N Ver 01.02.00.0i FTP server.\r\n"
    "220 SHARP MX-5001N Ver 01.05.00.0k FTP server.\r\n"
    "220 SHARP MX-M502N Ver 01.05.00.0m FTP server.\r\n"
    "220 SHARP MX-C312 Ver 01.05.00.0m FTP server.\r\n"
    "220 SHARP MX-4140N Ver 01.06.00.0f.01 FTP server.\r\n"
    "220 SHARP MX-5110N Ver 01.05.00.0m.80 FTP server.\r\n"
    "220 SHARP MX-M450N Ver 01.04.00.0g FTP server.\r\n"
    "220 SHARP MX-C312 Ver 01.05.00.0m FTP server.\r\n"
    "220 SHARP AR-M257 Ver 01.04.00.0e FTP server.\r\n"
    "220 SHARP MX-M550N Ver 01.04.00.0c FTP server.\r\n"
    "220 SHARP MX-C300W Ver 02.03.E1.00 FTP server.\r\n"
    "220 SHARP MX-M452N Ver 01.05.00.0k FTP server.\r\n"
    "220 SHARP MX-M452N Ver 01.05.00.0k FTP server.\r\n"
    "220 SHARP MX-2010U Ver 01.05.00.2k.51 FTP server.\r\n"
    "220 SHARP MX-2010U Ver 01.05.00.2k.56 FTP server.\r\n"
    "220 SHARP MX-2615N Ver 01.05.00.0q.06 FTP server.\r\n"
    "220 SHARP MX-M450U Ver 01.04.00.0e FTP server.\r\n"
    "220 SHARP MX-4101N Ver 01.05.00.0k FTP server.\r\n"
    "220 SHARP MX-M452N Ver 01.05.00.0k FTP server.\r\n"
    "220 SHARP MX-4112N Ver 01.05.00.0o.12 FTP server.\r\n"
    "220 SHARP MX-2300N Ver 01.02.00.0d FTP server.\r\n"
    "220 SHARP MX-2314N Ver 01.05.00.0q.06 FTP server.\r\n"
    "220 SHARP MX-3501N Ver 01.02.00.0e FTP server.\r\n"
    "220 SHARP MX-6240N Ver 01.06.00.00.107 FTP server.\r\n"
    "220 SHARP MX-2600FN Ver 01.05.00.0m FTP server.\r\n"
    "220 SHARP MX-2300N Ver 01.02.00.0i FTP server.\r\n"
    "220 SHARP MX-B400P Ver 01.05.00.0k FTP server.\r\n"
    "220 SHARP MX-5112N Ver 01.05.00.0o.12 FTP server.\r\n"
    "220 SHARP MX-2610N Ver 01.05.00.0m.93.U FTP server.\r\n"
    """
