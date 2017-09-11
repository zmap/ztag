from ztag.annotation import *


class HTTPServerParse(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    tests = {
      "nginx":{
        "local_metadata":{
          "product":"nginx",
          "version":"1.4.6"
        },
        "global_metadata":{
          "os":"Ubuntu"
        }
      },
      "iis7":{
        "local_metadata":{
          "manufacturer":"Microsoft",
          "product":"IIS",
          "version":"7.5"
        },
        "global_metadata":{
          "os":"Windows"
      },
      "nginx_simple":{
        "local_metadata":{
          "product":"nginx",
        }
      }
    }

    def process(self, obj, meta):
        s = obj["headers"]["server"]
        if "mini_httpd" in s:
            return
        m = self.http_banner_parse(s, meta)
        if "-" in m.local_metadata.product:
            manu, prod = m.local_metadata.product.split("-")
            m.local_metadata.manufacturer = manu
            m.local_metadata.product = prod
        elif m.local_metadata.product.lower() == "apache":
            m.local_metadata.manufacturer = "Apache"
            m.local_metadata.product = "httpd"
        elif m.local_metadata.product.lower() == "httpd":
            m.local_metadata.manufacturer = "Apache"
            m.local_metadata.product = "httpd"
        elif m.local_metadata.product.lower() == "ats":
            m.local_metadata.manufacturer = "Apache"
            m.local_metadata.product = "Traffic Server"
        elif m.local_metadata.product == "gws":
            m.local_metadata.manufacturer = "Google"
            m.local_metadata.product = "Web Server"
        elif m.local_metadata.product == "ghs":
            m.local_metadata.manufacturer = "Google"
            m.local_metadata.product = "Hosted Site"
        elif m.local_metadata.product == "bigip":
            m.local_metadata.manufacturer = "F5"
            m.local_metadata.product = "BigIP"
        elif m.local_metadata.product == "gse":
            m.local_metadata.manufacturer = "Google"
            m.local_metadata.product = "Scripting Engine"
        elif m.local_metadata.product == "GoAhead-Webs":
            m.tags.add("embedded")
        elif m.local_metadata.product == "RomPager":
            m.tags.add("embedded")
        elif m.local_metadata.product == "Mikrotik":
            m.global_metadata.manufacturer = Manufacturer.MIKROTIK
            m.tags.add("embedded")

        if m.global_metadata.os and "HTTP" in m.global_metadata.os:
            m.global_metadata.os = None
        if m.local_metadata.product == "IIS" or m.local_metadata.product == "Microsoft-IIS":
            m.global_metadata.os = "Windows"
        return m


