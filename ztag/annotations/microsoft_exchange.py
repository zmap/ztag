import re

from ztag.annotation import *

def _mprocess(self, obj, meta):
    if "Microsoft Exchange Server" not in obj["banner"]:
        return
    meta.global_metadata.os = OperatingSystem.WINDOWS
    meta.local_metadata.manufacturer = Manufacturer.MICROSOFT
    meta.local_metadata.product = "Exchange Server" 
    v = self.banner_re.search(obj["banner"])
    if v:
        v2 = v.groups(0)
        meta.local_metadata.version = v2[0]
    return meta


class MicrosoftExchangeMail(Annotation):

    tests = {
        "microsoft_exchange_2007":{
            "local_metadata":{
                "manufacturer":"Microsoft",
                "product":"Exchange Server",
                "version":"2007"
            },
            "global_metadata":{
                "os":OperatingSystem.WINDOWS
            }
        }
    }


class MicrosoftExchangePOP3X(MicrosoftExchangeMail):

    port = None 
    banner_re = re.compile("\+OK (?:Welcome to )?Microsoft Exchange (?:Server )?(2[0-9][0-9][0-9]) POP3")


class MicrosoftExchangePOP3S(MicrosoftExchangePOP3X):

    protocol = protocols.POP3S
    subprotocol = protocols.POP3S.TLS
    process = _mprocess


class MicrosoftExchangePOP3(MicrosoftExchangePOP3X):

    protocol = protocols.POP3
    subprotocol = protocols.POP3.STARTTLS
    process = _mprocess


class MicrosoftExchangeIMAPX(MicrosoftExchangeMail):

    port = None
    banner_re = re.compile("\* OK Microsoft Exchange (?:Server )?(2[0-9][0-9][0-9]) IMAP")


class MicrosoftExchangeIMAP(MicrosoftExchangeIMAPX):

    protocol = protocols.IMAP
    subprotocol = protocols.IMAP.STARTTLS
    process = _mprocess


class MicrosoftExchangeIMAPS(MicrosoftExchangeIMAPX):

    protocol = protocols.IMAPS
    subprotocol = protocols.IMAPS.TLS
    process = _mprocess


class MicrosoftExchangeSMTP(Annotation):

    port = None
    protocol = protocols.SMTP
    subprotocol = protocols.SMTP.STARTTLS

    tests = {
        "microsoft_exchange_2007":{
            "local_metadata":{
                "manufacturer":"Microsoft",
                "product":"Exchange Server",
            },
            "global_metadata":{
                "os":OperatingSystem.WINDOWS
            }
        }
    }

    def process(self, obj, meta):
        if "Microsoft ESMTP MAIL Service" in obj["banner"] or "Microsft Exchange" in obj["banner"]:
            meta.local_metadata.manufacturer = Manufacturer.MICROSOFT
            meta.local_metadata.product = "Exchange Server"
            meta.global_metadata.os = OperatingSystem.WINDOWS
            return meta



