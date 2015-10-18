from ztag.annotation import * 


class CommonIMAP(Annotation):

    protocol = protocols.IMAP
    subprotocol = protocols.IMAP.STARTTLS
    port = None

    def process(self, obj, meta):
        s_banner = obj["banner"]
        if "Dovecot" in s_banner:
            meta.local_metadata.product = "Dovecot"
            return meta
        elif "Courier-IMAP" in s_banner:
            meta.local_metadata.product = "Courier"
            return meta
        elif "Gimap" in s_banner:
            meta.local_metadata.manufacturer = "Google"
            meta.local_metadata.product = "IMAP"
            return meta
