from ztag.annotation import * 


class CommonPOP3(Annotation):

    protocol = protocols.POP3
    subprotocol = protocols.POP3.STARTTLS
    port = None

    def process(self, obj, meta):
        s_banner = obj["banner"]
        if "Dovecot" in s_banner:
            meta.local_metadata.product = "Dovecot"
            return meta
        elif "MailEnable" in s_banner:
            meta.local_metadata.product = "MailEnable"
            return meta
        elif "Gpop" in s_banner:
            meta.local_metadata.manufacturer = "Google"
            meta.local_metadata.product = "POP3"
            return meta
