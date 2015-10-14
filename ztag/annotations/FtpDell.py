import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpDell(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    printer_1_re = re.compile(
        "^220 (\w+ )?Dell (\w+ )?Laser Printer",
        re.IGNORECASE
        )
    product_1_re = re.compile(
        "^220 ET[0-9A-Z]+ Dell (\w+ Laser) Printer",
        re.IGNORECASE
        )

    printer_2_re = re.compile(
        "^220 Dell (\w+ )?Color Laser",
        re.IGNORECASE
        )
    product_2_re = re.compile(
        "^220 Dell (?:Color )?Laser(?: Printer)? (\w+)",
        re.IGNORECASE
        )

    tests = {
        "FtpDell_1": {
            "global_metadata": {
                "device_type": Type.LASER_PRINTER,
                "manufacturer": Manufacturer.DELL,
                "product": "B2360dn Laser"
            }
        },
        "FtpDell_2": {
            "global_metadata": {
                "device_type": Type.LASER_PRINTER,
                "manufacturer": Manufacturer.DELL,
                "product": "5110cn"
            }
        }
    }


    def process(self, obj, meta):
        banner = obj["banner"]

        if self.printer_1_re.search(banner):
            meta.global_metadata.device_type = Type.LASER_PRINTER
            meta.global_metadata.manufacturer = Manufacturer.DELL

            product = self.product_1_re.search(banner).group(1)
            meta.global_metadata.product = product

            return meta


        if self.printer_2_re.search(banner):
            meta.global_metadata.device_type = Type.LASER_PRINTER
            meta.global_metadata.manufacturer = Manufacturer.DELL

            product = self.product_2_re.search(banner).group(1)
            meta.global_metadata.product = product

            return meta

    """ Tests
    "220 ET0021B7A1AAF8 Dell B2360dn Laser Printer FTP Server NH41.CY.N454 ready.\r\n"
    "220 ET0021B73644D6 Dell B2360dn Laser Printer FTP Server NW1.CY.N151 ready.\r\n"
    "220 ET0021B7025E6A Dell 5350dn Laser Printer FTP Server NR.APS.N528 ready.\r\n"
    "220 Dell Color Laser 5110cn\r\n"
    "220 ET00040009BD28 Dell Laser Printer 5310n FTP Server NS.NP.N224 ready.\r\n"
    "220 Dell Laser Printer 5100cn\r\n"
    "220 Dell Color Laser 1320c\r\n"
    "220 Dell Color Laser 5110cn\r\n"
    "220 ET00040065D157 Dell Laser Printer 1710n FTP Server BR.Q.P204 ready.\r\n"
    "220 ET0004002DB976 Dell Laser Printer 1710n FTP Server BR.Q.P203 ready.\r\n"
    "220 Dell Color Laser 3110cn\r\n"
    "220 ET0021B7864744 Dell 5350dn Laser Printer FTP Server NR.APS.N644 ready.\r\n"
    "220 Dell Color Laser 3110cn\r\n"
    "220 ET0021B7C15CCC Dell B2360dn Laser Printer FTP Server NH.CY.N328 ready.\r\n"
    "220 ET0021B794F74A Dell 3330dn Laser Printer FTP Server NR.APS.N447b2 ready.\r\n"
    "220 ET000400DEA64A Dell Laser Printer 5210n FTP Server NS.NP.N240 ready.\r\n"
    """
