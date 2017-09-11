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
            meta.tags.add("embedded")
            return meta


class HPPrinterHTTPSOrg(TLSTag):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    def process(self, obj,meta):
        cn = obj["certificate"]["parsed"]["issuer"]["organization"][0]
        if org == "Hewlett-Packard Co.":
            meta.global_metadata.manufacturer = Manufacturer.HP
            meta.global_metadata.device_type = Type.PRINTER
            meta.tags.add("embedded")
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
      # "title": " hp LaserJet 1320 series /\n141.212.25.193 "
      "hp_laserjet_1320":{
        "global_metadata":{
          "manufacturer":Manufacturer.HP,
          "device_type":Type.PRINTER,
          "product":"LaserJet 1320",
        },
        "tags":["embedded",]
      },
      # \nHP LaserJet P3005 Printers
      "hp_laserjet_p3005":{
        "global_metadata":{
          "manufacturer":Manufacturer.HP,
          "device_type":Type.PRINTER,
          "product":"LaserJet P3005",
        },
        "tags":["embedded",]
      },
      # \nHP Color LaserJet 4700 Printers
      "hp_laserjet_4700":{
        "global_metadata":{
          "manufacturer":Manufacturer.HP,
          "device_type":Type.PRINTER,
          "product":"Color LaserJet 4700",
        },
        "tags":["embedded",]
      },
      # "title": "HP LaserJet 400 M401dn&nbsp;&nbsp;&nbsp;141.212.89.22"
      "hp_laserjet_400":{
        "global_metadata":{
          "manufacturer":Manufacturer.HP,
          "device_type":Type.PRINTER,
          "product":"LaserJet 400 M401dn",
        },
        "tags":["embedded",]
      },
      # "title": "HP Officejet Pro L7500"
      "hp_officejet_pro_l7500":{
        "global_metadata":{
          "manufacturer":Manufacturer.HP,
          "device_type":Type.PRINTER,
          "product":"Officejet Pro L7500",
        },
        "tags":["embedded",]
      },
      # "title": "HP Color LaserJet MFP M476dw&nbsp;&nbsp;&nbsp;141.212.190.116
      "hp_color_laserjet_mfp_m476dw":{
        "global_metadata":{
          "manufacturer":Manufacturer.HP,
          "device_type":Type.PRINTER,
          "product":"Color LaserJet MFP M476dw",
        },
        "tags":["embedded",]
      },
      # "HP LaserJet P4014 Printers"
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
        title = obj["title"].strip()
        t_l = title.lower()
        if t_l.startswith("hp")\
                and ("printer" in t_l or "laser" in t_l or "jet" in t_l):
            if "&nbsp;" in title:
                title = title.split("&nbsp;")[0]
            if "/" in title:
                title = title.split("/")[0]
            title = title.replace("Printers","").strip()
            title = title.replace("Printer","").strip()
            title = title.replace("Series","").strip()
            title = title.replace("series","").strip()
            title = title.replace("HP","").strip()
            title = title.replace("hp","").strip()
            meta.global_metadata.manufacturer = Manufacturer.HP
            meta.global_metadata.device_type = Type.PRINTER
            meta.tags.add("embedded")
            if title:
                meta.global_metadata.product = title
            return meta

