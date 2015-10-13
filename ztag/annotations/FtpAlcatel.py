import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test


class FtpAlcatel(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None
    manufact_re = re.compile("ALCATEL SR 7750")

    def process(self, obj, meta):
        banner = ob["banner"]
        tagged = False

        if self.manufact_re.search(banner):
            meta.global_metadata.device_type = Type.INFRASTRUCTURE_ROUTER
            meta.global_metadata.manufacturer = Manufacturer.ALCATEL
            meta.global_metadata.product = "SR 7750"
            tagged = True

        if tagged:
            return meta
        else:
            return None

    """ Tests
    "220-TiMOS-C-12.0.R4 cpm/hops64 ALCATEL SR 7750 Copyright (c) 2000-2014 Alcatel-Lucent.\r\n220-All rights reserved. All use subject to applicable license agreements.\r\n220-Built on Tue Jul 29 16:26:06 PDT 2014 by builder in /rel12.0/b1/R4/panos/main\r\n220-\r\n220- %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\r\n220-\r\n220-                               - W A R N I N G -\r\n220-\r\n220-                                                                                                                                                                    A notice that any unauthorized use of the system is unlawful,\r\n220-            and may be subject to civil and/or criminal penalties.\r\n220-\r\n220-\r %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% \r\n220 FTP server ready\r\n"
    "220-TiMOS-C-9.0.R6 cpm/hops ALCATEL SR 7750 Copyright (c) 2000-2011 Alcatel-Lucent.\r\n220-All rights reserved. All use subject to applicable license agreements.\r\n220-Built on Tue Sep 27 12:38:04 PDT 2011 by builder in /rel9.0/b1/R6/panos/main\r\n220-\r\n220 FTP server ready\r\n"
    "220-TiMOS-C-11.0.R14 cpm/hops ALCATEL SR 7750 Copyright (c) 2000-2014 Alcatel-Lucent.\r\n220-All rights reserved. All use subject to applicable license agreements.\r\n220-Built on Sun Dec 14 10:49:07 PST 2014 by builder in /rel11.0/b1/R14/panos/main\r\n220-\r\n220 FTP server ready\r\n"
    "220-TiMOS-C-10.0.R12 cpm/hops ALCATEL SR 7750 Copyright (c) 2000-2013 Alcatel-Lucent.\r\n220-All rights reserved. All use subject to applicable license agreements.\r\n220-Built on Tue Jun 25 14:51:31 PDT 2013 by builder in /rel10.0/b1/R12/panos/main\r\n220-\r\n220-WARNING!!! Authorised access only, all of your done will be recorded! disconnect IMMEDIATELY if you are not an authorised user!\r\n220 FTP server ready\r\n"
    "220-TiMOS-C-8.0.R10 cpm/hops ALCATEL SR 7750 Copyright (c) 2000-2011 Alcatel-Lucent.\r\n220-All rights reserved. All use subject to applicable license agreements.\r\n220-Built on Tue May 24 17:48:05 PDT 2011 by builder in /rel8.0/b1/R10/panos/main\r\n220-\r\n220 FTP server ready\r\n"
    "220-TiMOS-C-8.0.R10 cpm/hops ALCATEL SR 7750 Copyright (c) 2000-2011 Alcatel-Lucent.\r\n220-All rights reserved. All use subject to applicable license agreements.\r\n220-Built on Tue May 24 17:48:05 PDT 2011 by builder in /rel8.0/b1/R10/panos/main\r\n220-\r\n220 FTP server ready\r\n"
    "220-TiMOS-C-8.0.R6 cpm/hops ALCATEL SR 7750 Copyright (c) 2000-2010 Alcatel-Lucent.\r\n220-All rights reserved. All use subject to applicable license agreements.\r\n220-Built on Thu Nov 11 20:27:48 PST 2010 by builder in /rel8.0/b1/R6/panos/main\r\n220-\r\n220 FTP server ready\r\n"
    "220-TiMOS-C-8.0.R10 cpm/hops ALCATEL SR 7750 Copyright (c) 2000-2011 Alcatel-Lucent.\r\n220-All rights reserved. All use subject to applicable license agreements.\r\n220-Built on Tue May 24 17:48:05 PDT 2011 by builder in /rel8.0/b1/R10/panos/main\r\n220-\r\n220 FTP server ready\r\n"
    "220-TiMOS-C-8.0.R10 cpm/hops ALCATEL SR 7750 Copyright (c) 2000-2011 Alcatel-Lucent.\r\n220-All rights reserved. All use subject to applicable license agreements.\r\n220-Built on Tue May 24 17:48:05 PDT 2011 by builder in /rel8.0/b1/R10/panos/main\r\n220-\r\n220 FTP server ready\r\n"
    "220-TiMOS-C-8.0.R10 cpm/hops ALCATEL SR 7750 Copyright (c) 2000-2011 Alcatel-Lucent.\r\n220-All rights reserved. All use subject to applicable license agreements.\r\n220-Built on Tue May 24 17:48:05 PDT 2011 by builder in /rel8.0/b1/R10/panos/main\r\n220-\r\n220 FTP server ready\r\n"
    """
