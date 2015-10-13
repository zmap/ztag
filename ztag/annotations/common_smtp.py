from ztag.annotation import * 


class CommonSMTP(Annotation):

    protocol = protocols.SMTP
    subprotocol = protocols.SMTP.STARTTLS
    port = None

    def process(self, obj, meta):
        s_banner = obj["banner"][4:]
        if "Postfix" in s_banner:
            meta.local_metadata.product = "Postfix"
            return meta
        elif "Sendmail" in s_banner:
            meta.local_metadata.product = "Sendmail"
            return meta
