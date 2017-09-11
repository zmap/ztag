from ztag.annotation import *

class LenovoHTTPLogo(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        if '<img id="logo" src="/manage/images/logo.png" alt="LenovoEMC"/>' in obj["body"]:
            meta.global_metadata.manufacturer = Manufacturer.LENOVO
            meta.tags.add("embedded")
            return meta
