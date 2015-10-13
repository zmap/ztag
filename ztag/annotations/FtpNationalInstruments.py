from ztag.annotation import Annotation
from ztag import protocols
import ztag.test


class FtpNationalInstruments(Annotation):
    name = "NationalInstruments"
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    def process(self, obj, meta):
        banner = obj["banner"]

        if banner.startwith("220-National Instruments FTP"):
            meta.global_metadata.manufacturer = Manufacturer.NATIONAL_INSTRUMENTS

        return meta
