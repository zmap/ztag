from ztag.annotation import *


class STARTTLSStrip(TLSTag):

    protocol = protocols.SMTP
    subprotocol = protocols.HTTPS.STARTTLS
    port = None

    tests = {
        "stripstarttls":{"tags":["strip-starttls"]}
    }

    def process(self, obj, meta):
        stripped = False
        ehlo = obj["ehlo"]
        if "XXXX" in ehlo and "STARTTLS" not in ehlo:
            stripped = True
        if "XXXX" in obj["starttls"]:
            stripped = True
        if stripped:
            meta.tags.add("strip-starttls")
            return meta


