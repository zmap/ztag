from ztag.annotation import *
import re

class FtpAxis(Annotation):

    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    camera_manufact_re = re.compile(
                        "^220 AXIS .*Network .*Camera",
                        re.IGNORECASE
                        )
    vid_encode_manufact_re = re.compile(
                        "^220 AXIS [^\s]* Video Encoder",
                        re.IGNORECASE
                        )
    product_re = re.compile("^220 AXIS (.+) \d+\.\d+", re.IGNORECASE)
    manufact_re = re.compile("^220 AXIS .* ready", re.IGNORECASE)

    def process(self, obj, meta):
        banner = obj["banner"]
        tagged = False

        if self.camera_manufact_re.search(banner):
            meta.global_data.device_type = Type.CAMERA
            meta.global_data.manufacturer = Manufacturer.AXIS
            meta.global_data.product = self.product_re.search(banner).group(1)
            tagged = True

        if self.vid_encode_manufact_re.search(banner):
            meta.global_data.manufacturer = Manufacturer.AXIS
            meta.global_data.product = self.product_re.search(banner).group(1)
            tagged = True

        if self.manufact_re.search(banner):
            meta.global_data.manufacturer = Manufacturer.AXIS
            tagged = True

        if tagged:
            return meta
        else:
            return None

    """ Camera Tests
    "220 AXIS 221 Network Camera 4.45.1 (Mar 11 2008) ready.\r\n"
    "220 AXIS P1357 Network Camera 5.40.19.2 (2014) ready.\r\n"
    "220 AXIS P1357 Network Camera 5.40.19.1 (2013) ready.\r\n"
    "220 AXIS P3384-VE Network Camera 5.40.19 (2013) ready.\r\n"
    "220 AXIS 233D Network Dome Camera 4.48.4 (Mar 23 2010) ready.\r\n"
    "220 AXIS M3007 Network Camera 5.40.13.1 (2012) ready.\r\n"
    "220 AXIS Q6045-E PTZ Dome Network Camera 5.55.1 (2013) ready.\r\n"
    "220 AXIS M1011 Network Camera 5.00 (Dec 23 2008) ready.\r\n"
    "220 AXIS M1011 Network Camera 5.20.1 (Oct 25 2010) ready.\r\n"
    "220 AXIS P3344 Fixed Dome Network Camera 5.20 (Sep 21 2010) ready.\r\n"
    "220 AXIS P1346 Network Camera 5.40.9.2 (2012) ready.\r\n"
    "220 AXIS M3014 Network Fixed Dome Camera 5.05 (Jun 23 2009) ready.\r\n"
    "220 AXIS M1011 Network Camera 5.20.1 (Oct 25 2010) ready.\r\n"
    "220 Axis 2100 Network Camera 2.43 Nov 08 2004 ready.\r\n"
    "220 AXIS 210A Network Camera 4.40.1 (Sep 11 2007) ready.\r\n"
    "220 AXIS P5414-E PTZ Dome Network Camera 5.55.1.3 (2014) ready.\r\n"
    "220 AXIS 213 PTZ Network Camera 4.35 (Apr 04 2007) ready.\r\n"
    "220 AXIS M1011 Network Camera 5.00.1 (Dec 22 2009) ready.\r\n"
    """

    """ Video Encoder Tests
    "220 AXIS M7001 Video Encoder 5.20.1_cst_412205_1 (Dec 13 2013) ready.\r\n"
    "220 AXIS M7014 Video Encoder 5.40.7.1 (2012) ready.\r\n"
    "220 AXIS M7014 Video Encoder 5.40.6.1 (2011) ready.\r\n"
    "220 AXIS Q7401 Video Encoder 5.20.3 (Oct 12 2011) ready.\r\n"
    "220 AXIS M7014 Video Encoder 5.50.2 (2013) ready.\r\n"
    "220 AXIS M7001 Video Encoder 5.02 (Feb 10 2009) ready.\r\n"
    "220 AXIS M7014 Video Encoder 5.50.4 (2014) ready.\r\n"
    "220 AXIS Q7401 Video Encoder 5.50.4 (2014) ready.\r\n"
    "220 AXIS Q7401 Video Encoder 5.50.2 (2013) ready.\r\n"
    "220 AXIS Q7424-R Video Encoder 5.40.10 (2012) ready.\r\n"
    "220 AXIS Q7401 Video Encoder 5.50.2 (2013) ready.\r\n"
    "220 AXIS Q7406 Video Encoder Blade 5.11 (Apr 30 2010) ready.\r\n"
    "220 AXIS Q7404 Video Encoder 5.50.4 (2014) ready.\r\n"
    "220 AXIS Q7401 Video Encoder 5.01 (Aug 01 2008) ready.\r\n"
    "220 AXIS Q7401 Video Encoder 5.50.2 (2013) ready.\r\n"
    "220 AXIS M7014 Video Encoder 5.40.6.1 (2011) ready.\r\n"
    "220 AXIS Q7436 Video Encoder Blade 5.55.3.5 (2014) ready.\r\n"
    """
