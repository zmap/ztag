from ztag.annotation import Annotation
from ztag import protocols

import ztag.test


class GordianServer(Annotation):

	protocol = protocols.HTTP
	subprotocol = protocols.HTTP.GET
	port = None

	vals = {
		"software_name": "Gordian Embedded",
	}
	

	def process(self, obj, meta):	
            # looks like: Boa/0.94.14rc19
            server = obj["headers"]["server"]	
            if "gordian embedded" in server.lower():
                meta.local_metadata.product = "Gordian Embedded"
                index = server.lower().find("embedded") + len("embedded")
                if index < len(server):
                    meta.local_metadata.version = server[index:]
                return meta
            return None
