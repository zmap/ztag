from ztag.annotation import Annotation
from ztag import protocols
import ztag.test

class UCLinux(Annotation):
    name = "UCLinux"
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    def process(self, obj, meta):
        banner = obj["banner"]

        if "uClinux" in banner:
            meta.global_metadata.os = OperatingSystem.UCLINUX
            if "ARM7" in banner:
                meta.tags.append("Uses ARM7 chipset")

        return meta
