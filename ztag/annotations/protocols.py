from ztag.annotation import Annotation

from ztag import protocols

def __process(self, obj, meta):
    meta.tags.add(self.protocol.pretty_name)
    return meta

PROTOCOLS = [
    (protocols.HTTP, protocols.HTTP.GET, {"device_with_http":{"tags":["http",]}}),
    (protocols.FTP, protocols.FTP.BANNER, {"device_with_ftp":{"tags":["ftp",]}}),
    (protocols.HTTPS, protocols.HTTPS.TLS, {"device_with_https":{"tags":["https",]}}),
    (protocols.DNS, protocols.DNS.OPEN_RESOLVER, {"device_with_dns":{"tags":["dns",]}}),
    (protocols.UPNP, protocols.UPNP.DISCOVERY, {"device_with_upnp":{"tags":["upnp",]}}),
    (protocols.SSH, protocols.SSH.BANNER, {"device_with_ssh":{"tags":["ssh",]}}),
    (protocols.NTP, protocols.NTP.TIME, {"device_with_ntp":{"tags":["ntp",]}}),
    (protocols.IMAP, protocols.IMAP.STARTTLS, {"device_with_imap":{"tags":["imap",]}}),
    (protocols.IMAPS, protocols.IMAPS.TLS, {"device_with_imaps":{"tags":["imaps",]}}),
    (protocols.POP3, protocols.POP3.STARTTLS, {"device_with_pop3":{"tags":["pop3",]}}),
    (protocols.POP3S, protocols.POP3S.TLS, {"device_with_pop3s":{"tags":["pop3s",]}}),
    (protocols.SMTP, protocols.SMTP.STARTTLS, {"device_with_smtp":{"tags":["smtp",]}}),
    (protocols.SMTPS, protocols.SMTPS.TLS, {"device_with_smtps":{"tags":["smtps",]}}),
    (protocols.MODBUS, protocols.MODBUS.DEVICE_ID, {"device_with_modbus":{"tags":["modbus",]}}),
]

for proto, subproto, tests in PROTOCOLS:
    c = type("%s_annotation" % proto.pretty_name, (Annotation,), {"process":__process})
    c.protocol = proto
    c.subprotocol = subproto
    c.tests = tests
