from ztag.annotation import *

class Cougar(Annotation):

      protocol = protocols.HTTP
      subprotocol = protocols.HTTP.GET
      port = None

      def process(self, obj, meta):
          server = d["headers"]["server"]    
          if server[:6] == "Cougar":
              meta.local_metadata.product = "Cougar"
              if "/" in server:
                  meta.local_metadata.version = server.split("/", 1)[1]
              return meta

