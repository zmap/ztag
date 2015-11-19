from ztag.transform import ZMapTransform, ZMapTransformOutput
from ztag import protocols, errors

class DNSTransform(ZMapTransform):

    CORRECT_RESPONSE = "192.150.186.1"
    port = None
    protocol = protocols.DNS
    subprotocol = protocols.DNS.LOOKUP

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

        response_types = (("answers", "dns_answers"), ("authorities", "dns_authorities"),\
            ("additionals", "dns_additionals"))

        for out_field, obj_field in response_types:
            (response_errors, responses) = self._transform_responses(obj[obj_field])
            if response_errors:
                errors_present = True
            out[out_field] = responses

        out["errors"] = errors_present
        out["open_resolver"] = bool(len(out["answers"]) + len(out["additionals"]) + \
            len(out["authorities"]))
        out["resolves_correctly"] = False

        for answer in out["answers"]:
            if answer["type"] == "A" and answer["response"] == CORRECT_RESPONSE:
                out["resolves_correctly"] = True
                break

        zout.transformed = out
        return zout
