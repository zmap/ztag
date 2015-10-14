from ztag.annotation import Annotation
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpNationalInstruments(Annotation):
    name = "NationalInstruments"
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    tests = {
        "FtpNationalInstruments_1": {
            "global_metadata": {
                "manufacturer": Manufacturer.NATIONAL_INSTRUMENTS
            }
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if banner.startswith("220-National Instruments FTP"):
            meta.global_metadata.manufacturer = Manufacturer.NATIONAL_INSTRUMENTS

            return meta
