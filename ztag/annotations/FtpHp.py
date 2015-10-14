import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpHp(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    manufact_1_re = re.compile(
        "^220 HP ARPA FTP SERVER",
        re.IGNORECASE
        )

    manufact_2_re = re.compile(
        "The HPRC FTP dropbox system is intended for Hewlett-Packa",
        re.IGNORECASE
        )

    manufact_3_re = re.compile("^220 JD FTP Server Ready", re.IGNORECASE)

    tests = {
        "FtpHp_1": {
            "global_metadata": {
                "manufacturer": Manufacturer.HP
            },
            "local_metadata": {
                "product": "HP ARPA"
            }
        },
        "FtpHp_2": {
            "global_metadata": {
                "manufacturer": Manufacturer.HP
            },
            "local_metadata": {
                "product": "HP HPRC"
            }
        },
        "FtpHp_3": {
            "global_metadata": {
                "manufacturer": Manufacturer.HP,
                "device_type": Type.GENERIC_PRINTER,
            },
            "local_metadata": {
                "product": "Jet Direct"
            }
        },
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.manufact_1_re.search(banner):
            meta.global_metadata.manufacturer = Manufacturer.HP

            meta.local_metadata.product = "HP ARPA"

        if self.manufact_2_re.search(banner):
            meta.global_metadata.manufacturer = Manufacturer.HP

            meta.local_metadata.product = "HP HPRC"

        if self.manufact_3_re.search(banner):
            meta.global_metadata.device_type = Type.GENERIC_PRINTER
            meta.global_metadata.manufacturer = Manufacturer.HP
            meta.local_metadata.product = "Jet Direct"

        return meta

    """ Tests
    "220 HP ARPA FTP Server [A0010L09] (C) Hewlett-Packard Co. 2000 [PASV SUPPORT]\r\n"
    "220 HP ARPA FTP Server [A0012H15] (C) Hewlett-Packard Co. 2000 [PASV SUPPORT]\r\n"
    "220 HP ARPA FTP Server [A0012H15] (C) Hewlett-Packard Co. 2000 [PASV SUPPORT]\r\n"
    "220 HP ARPA FTP Server [A0009001] (C) Hewlett-Packard Co. 1990\r\n"
    "220------------------------------------------------------------------\r\n220-  The HPRC FTP dropbox system is intended for Hewlett-Packard \r\n220-  company business with authorized partners and customers.  The \r\n220-  terms and conditions for use of the system are published at\r\n220-     http://h3.usa.hp.com/\r\n220-  Use of HPRC implies acceptance of these terms and conditions.\r\n220-                                                  -- Thank you.\r\n220------------------------------------------------------------------\r\n220 HPRC FTP Server System\r\n"
    "220------------------------------------------------------------------\r\n220-  The HPRC FTP dropbox system is intended for Hewlett-Packard \r\n220-  company business with authorized partners and customers.  The \r\n220-  terms and conditions for use of the system are published at\r\n220-     http://ftp.usa.hp.com/\r\n220-  Use of HPRC implies acceptance of these terms and conditions.\r\n220-                                                  -- Thank you.\r\n220------------------------------------------------------------------\r\n220 HPRC FTP Server System\r\n"
    "220------------------------------------------------------------------\r\n220-  The HPRC FTP dropbox system is intended for Hewlett-Packard \r\n220-  company business with authorized partners and customers.  The \r\n220-  terms and conditions for use of the system are published at\r\n220-     http://h1.usa.hp.com/\r\n220-  Use of HPRC implies acceptance of these terms and conditions.\r\n220-                                                  -- Thank you.\r\n220------------------------------------------------------------------\r\n220 HPRC FTP Server System\r\n"
    "220------------------------------------------------------------------\r\n220-  The HPRC FTP dropbox system is intended for Hewlett-Packard \r\n220-  company business with authorized partners and customers.  The \r\n220-  terms and conditions for use of the system are published at\r\n220-     http://h1-itg.usa.hp.com/\r\n220-  Use of HPRC implies acceptance of these terms and conditions.\r\n220-                                                  -- Thank you.\r\n220------------------------------------------------------------------\r\n220 HPRC FTP Server System\r\n"
    "220 JD FTP Server Ready\r\n"
    "220 JD FTP Server Ready\r\n"
    "220 JD FTP Server Ready\r\n"
    "220 JD FTP Server Ready\r\n"
    """
