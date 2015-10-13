from ztag.transform import ZMapTransform, ZMapTransformOutput
from ztag import protocols, errors


class DNSTransform(ZMapTransform):

    name = "dns/open_resolver"
    port = None
    protocol = protocols.DNS
    subprotocol = protocols.DNS.OPEN_RESOLVER

    def __init__(self, *args, **kwargs):
        super(DNSTransform, self).__init__(*args, **kwargs)

    def _transform_object(self, obj):
        classification = obj['classification']
        if classification != "dns":
            raise errors.IgnoreObject(classification)
        if int(obj['success']) != 1 or int(obj['app_success']) != 1:
            raise errors.IgnoreObject("Not a DNS resposne")
        zout = ZMapTransformOutput()
        out = dict()
        out["support"] = True
        out["recursive_resolver"] = bool(len(obj["dns_answers"]))
        out["iterative_resolver"] = bool(len(obj["dns_authorities"]))
        if out["recursive_resolver"]:
            answers = []
            errors_present = False
            for answer in obj["dns_answers"]:
                if answer["rdata_is_parsed"] == 1:
                    answers.append(answer["rdata"])
                else:
                    errors_present = True
                    break
            if not errors_present:
                out["answers"] = answers
        if out["iterative_resolver"]:
            authorities = []
            errors_present = False
            for authority in obj["dns_authorities"]:
                 if authority["rdata_is_parsed"] == 1:
                    authorities.append(authority["rdata"])
                 else:
                    errors_present = True
                    break
            if not errors_present:
                out["authorities"] = authorities 
        out['ip_address'] = obj['saddr']
        out['timestamp'] = obj['timestamp-str']
        zout.transformed = out
        return zout
