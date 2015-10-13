from ztag.annotation import * 

class AmericanMegatrends(Annotation):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    tests = {
        "american_megatrends":{
            "local_metadata":{
                "manufacturer": Manufacturer.AMERICANMEGATRENDS
            }
        }
    }

    def process(self, obj, meta):
        organization = obj["certificate"]["parsed"]["subject"]["organization"][0]
        if "American Megatrends Inc" in organization:
            meta.local_metadata.manufacturer = Manufacturer.AMERICANMEGATRENDS
            return meta

