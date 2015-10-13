from ztag.annotation import Annotation

from ztag import protocols
#from ztag.devices import schneider

import ztag.test


#class ModbusTag(Annotation):
#
#    name = "HTTP"
#
#    protocol = protocols.MODBUS
#    subprotocol = None
#    port = None
#
#    tags = [
#        "modbus",
#    ]
#
#    def _process(self, d):
#        return (self.tags, {})
#

class MicrosoftHttpAPI(Annotation):

    	name = "Microsoft HTTPAPI"

    	protocol = protocols.HTTP
    	subprotocol = protocols.HTTP.GET
    	port = None


    	def _process(self, d):	
        	server = d["http_headers"]["server"]	
        	#if server.lower().find("(") != -1 & server.lower().find("/") != -1:
        	if server.lower().find("microsoft-httpapi") != -1:
			found_version = 0
			slash = server.find("/")
			version = ""
			# If there is a slash, then there is a version number
			if slash != -1:
				found_version = 1
				version = server[slash+1:]
			# Need to print out appropriate 
			vals_complete = {}
			if found_version:
				vals_complete = {
					"software_vendor": "Microsoft",
					"software_name": "Microsoft-HTTPAPI",
					"software_version": version,
				}
			else:
				vals_complete = {
					"software_vendor": "Microsoft",
					"software_name": "Microsoft-HTTPAPI",
				}
            		return ([], vals_complete)


#class TestScheniderMEITag(ztag.test.TagTestCase):
#
#    devices = {
#        schneider.M340BMXNOE0100: ([], SchneiderMEITag.vals),
#    }
#
#    tag = SchneiderMEITag
