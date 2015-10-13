from ztag.annotation import * 


class MicrosoftWinCE(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None


    def process(self, obj, meta):
        s = obj["headers"]["server"]
        if "Microsoft-WinCE" in s:
            meta.local_metadata.manufacturer = Manufactuer.MICROSOFT
            meta.local_metadata.product = "Windows CE" 
            meta.global_metadata.os = OperatingSystem.WINDOWS
            if "/" in s:
                val = s.split("/")[1].strip()
                meta.local_metadata.version = val
                meta.global_metadata.os_version = val
            return meta
