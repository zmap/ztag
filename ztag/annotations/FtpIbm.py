import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpIbm(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    ibm_re = re.compile(
        "^220-QTCP at .*\r\n220 Connection will close if idle more than \d+ minutes",
        re.IGNORECASE
        )

    tests = {
        "FtpIbm_1": {
            "global_metadata": {
                "manufacturer": Manufacturer.IBM,
                "product": "IBM I-series"
            }
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.ibm_re.search(banner):
            meta.global_metadata.manufacturer = Manufacturer.IBM
            meta.global_metadata.product = "IBM I-series"

        return meta

    """ Tests
    "220-QTCP at DUTYMS.CO.UK.\r\n220 Connection will close if idle more than 5 minutes.\r\n"
    "220-QTCP at host228-116.static83.221.interbusiness.it.\r\n220 Connection will close if idle more than 5 minutes.\r\n"
    "220-QTCP at DKSRV117.\r\n220 Connection will close if idle more than 5 minutes.\r\n"
    "220-QTCP at ISERIES.\r\n220 Connection will close if idle more than 300 minutes.\r\n"
    "220-QTCP at IPADEMO.\r\n220 Connection will close if idle more than 30 minutes.\r\n"
    "220-QTCP at myduncan.aero.\r\n220 Connection will close if idle more than 5 minutes.\r\n"
    "220-QTCP at PEGASUS1.\r\n220 Connection will close if idle more than 5 minutes.\r\n"
    "220-QTCP at S06BF464.\r\n220 Connection will close if idle more than 20 minutes.\r\n"
    "220-QTCP at S100E254.\r\n220 Connection will close if idle more than 5 minutes.\r\n"
    "220-QTCP at ISERVER1.\r\n220 Connection will close if idle more than 5 minutes.\r\n"
    "220-QTCP at srvdemo.smeup.com.\r\n220 Connection will close if idle more than 5 minutes.\r\n"
    "220-QTCP at S103NZWM.APPN.SNA.IBM.COM.\r\n220 Connection will close if idle more than 5 minutes.\r\n"
    "220-QTCP at 218.151.149.50.\r\n220 Connection will close if idle more than 5 minutes.\r\n"
    """
