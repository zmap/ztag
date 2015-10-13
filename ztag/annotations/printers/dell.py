from ztag.annotation import *

class DellPrinterHTTPS(Annotation):

    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    def process(self, obj, meta):
        cn = obj["certificate"]["parsed"]["subject"]["common_name"][0]
        if "Dell" in cn and "Printer" in cn:
            meta.global_metadata.device_type = Type.LASER_PRINTER
            meta.global_metadata.manufacturer = Manufacturer.DELL
            meta.tags.add("printer")
            meta.tags.add("embedded")
            if cn != "Dell Laser Printer":
                p = cn.split(" ")[1]
                meta.global_metadata.product = p
            return meta
