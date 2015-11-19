from ztag.transform import ZMapTransform, ZMapTransformOutput
from ztag import protocols, errors

CORRECT_RESPONSE = "192.150.186.1"

class DNSTransform(ZMapTransform):

    name = "dns/open"
    port = None
    protocol = protocols.DNS
    subprotocol = protocols.DNS.OPEN_RESOLVER

    def __init__(self, *args, **kwargs):
        super(DNSTransform, self).__init__(*args, **kwargs)

    def _transform_responses(self, responses):
        error = False
        ret = []

        for response in responses:
            if response["rdata_is_parsed"] == 1:
                r = dict()
                r["name"] = response["name"]
                r["type"] = response["type_str"]
                r["response"] = response["rdata"]
                ret.append(r)
            else:
                error = True

        return (error, ret)

    def _transform_object(self, obj):
        classification = obj['classification']
        if classification != "dns":
            raise errors.IgnoreObject(classification)
        if int(obj['success']) != 1:
            raise errors.IgnoreObject("Not a DNS resposne")
        zout = ZMapTransformOutput()
        out = dict()
        out["supports"] = True
        errors_present = False

        if obj["dns_parse_err"] == True:
            errors_present = True

        out["questions"] = []

        for question in obj["dns_questions"]:
            q = dict()
            q["name"] = question["name"]
            q["type"] = question["qtype_str"]
            out["questions"].append(q)

        for field in ("answers", "authorities", "additionals"):
            (response_errors, responses) = self._transform_responses(obj["dns_%s" % field])
            if response_errors:
                errors_present = True
            out[field] = responses

        out["errors"] = errors_present
	out["open_resolver"] = bool(len(out["answers"] + out["additionals"] + out["authorities"]))
        out["resolves_correctly"] = False

        for answer in out["answers"]:
            if answer["type"] == "A" and answer["response"] == CORRECT_RESPONSE:
                out["resolves_correctly"] = True
                break

        zout.transformed = out
        return zout
