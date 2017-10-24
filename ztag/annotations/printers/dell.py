import re

from ztag.annotation import *

class DellPrinterHTTPS(Annotation):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
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



class DellPrinterHTTPTitleForm1(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    tests = {
      "dell_color_laser_3110cn":{
        "global_metadata":{
          "manufacturer":Manufacturer.DELL,
          "device_type":Type.LASER_PRINTER,
          "product":"Color Laser 3110cn",
        },
        "tags":["embedded",]
      }
    }

    def process(self, obj, meta):
        title = obj["title"].strip()
        if title.startswith("Dell Laser Printer")\
                or title.startswith("Dell MFP Laser")\
                or title.startswith("Dell Color Laser"):
            meta.global_metadata.manufacturer = Manufacturer.DELL
            meta.global_metadata.product = title.split(" ", 1)[1]
            meta.global_metadata.device_type = Type.LASER_PRINTER
            meta.tags.add("embedded")
            return meta
        if title in {"Dell Laser MFP", "Dell Laser LBP"}:
            meta.global_metadata.manufacturer = Manufacturer.DELL
            meta.global_metadata.product = "Laser Printer"
            meta.global_metadata.device_type = Type.LASER_PRINTER



class DellPrinterHTTPTitleForm2(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None


    model_re = re.compile("Dell (\w*) (Laser Printer|Color Laser|Laser MFP)")

    tests = {
      "dell_2130cn_color_laser":{
        "global_metadata":{
          "manufacturer":Manufacturer.DELL,
          "device_type":Type.LASER_PRINTER,
          "product":"Color Laser 2130cn",
        },
        "tags":["embedded",]
      },
      "dell_b2360dn_laser_printer":{
        "global_metadata":{
          "manufacturer":Manufacturer.DELL,
          "device_type":Type.LASER_PRINTER,
          "product":"Laser Printer B2360dn",
        },
        "tags":["embedded",]
      },
    }

    def process(self, obj, meta):
        t = obj["title"].strip()
        if t.startswith("Dell"):
            r = self.model_re.match(t)
            if r:
                meta.global_metadata.manufacturer = Manufacturer.DELL
                meta.global_metadata.device_type = Type.LASER_PRINTER
                meta.global_metadata.product = "%s %s" % (r.groups()[1],
                        r.groups()[0])
                meta.tags.add("embedded")
                return meta

