from ztag.annotation import *

class HPPrinterHTTPSCN(TLSTag):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    def process(self, obj,meta):
        cn = obj["certificate"]["parsed"]["issuer"]["common_name"][0]
        if "HP-Printers" in cn:
            meta.global_metadata.manufacturer = Manufacturer.HP
            meta.global_metadata.device_type = Type.PRINTER
            return meta


class HPPrinterHTTPSOrg(TLSTag):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    def process(self, obj,meta):
        cn = obj["certificate"]["parsed"]["issuer"]["organization"][0]
        if org == "Hewlett-Packard Co.":
            meta.global_metadata.manufacturer = Manufacturer.HP
            return meta



class HPPrinterHTTPHeader(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    tests = {
      "hp_printer_server":{
        "global_metadata":{
          "manufacturer":Manufacturer.HP,
          "device_type":Type.PRINTER,
          "product":"Officejet Pro 8620",
          "version":"A7F65A"
        },
        "tags":["embedded",]
      }
    }

    def process(self, obj, meta):
        s = obj["headers"]["server"]
        if "HP HTTP Server" in s:
            meta.global_metadata.manufacturer = Manufacturer.HP
            meta.global_metadata.device_type = Type.PRINTER
            meta.tags.add("embedded")
            if ";" in s:
                sp = s.split(";")
                if len(sp) < 2:
                    return meta
                product = sp[1].strip()
                if product.startswith("HP HP"):
                    product = product[6:]
                elif product.startswith("HP "):
                    product = product[3:]
                if "-" in product:
                    p = product.split("-")[0].strip()
                    model = product.split("-")[1].strip()
                    meta.global_metadata.product = p
                    meta.global_metadata.version = model
                else:
                    meta.global_metadata.product = product
            return meta


class HPPrinterHTTPTitle(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    tests = {
      "hp_laserjet_1320":{
        "global_metadata":{
          "manufacturer":Manufacturer.HP,
          "device_type":Type.PRINTER,
          "product":"LaserJet 1320",
        },
        "tags":["embedded",]
      },
      "hp_laserjet_p3005":{
        "global_metadata":{
          "manufacturer":Manufacturer.HP,
          "device_type":Type.PRINTER,
          "product":"LaserJet P3005",
        },
        "tags":["embedded",]
      },
      "hp_laserjet_4700":{
        "global_metadata":{
          "manufacturer":Manufacturer.HP,
          "device_type":Type.PRINTER,
          "product":"LaserJet 4700",
        },
        "tags":["embedded",]
      },
      "hp_laserjet_400":{
        "global_metadata":{
          "manufacturer":Manufacturer.HP,
          "device_type":Type.PRINTER,
          "product":"LaserJet 400",
          "version":"M401dn"
        },
        "tags":["embedded",]
      },
      "hp_officejet_pro_l7500":{
        "global_metadata":{
          "manufacturer":Manufacturer.HP,
          "device_type":Type.PRINTER,
          "product":"Officejet Pro L7500",
        },
        "tags":["embedded",]
      },
      "hp_color_laserjet_mfp_m476dw":{
        "global_metadata":{
          "manufacturer":Manufacturer.HP,
          "device_type":Type.PRINTER,
          "product":"Color LaserJet MFP M476dw",
        },
        "tags":["embedded",]
      },
      "hp_laserjet_p4014":{
        "global_metadata":{
          "manufacturer":Manufacturer.HP,
          "device_type":Type.PRINTER,
          "product":"LaserJet P4014",
        },
        "tags":["embedded",]
      },
    }

    def process(self, obj, meta):
        if "/media/canonlogo.gif" in obj["body"]:
            meta.global_metadata.manufacturer = Manufacturer.Canon
            meta.global_metadata.device_type = Type.PRINTER
            meta.tags.add("embedded")
            return meta

