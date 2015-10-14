import re
from ztag.annotation import Manufacturer
from ztag.annotation import Annotation
from ztag.annotation import Type
from ztag.annotation import OperatingSystem
from ztag import protocols
import ztag.test


class FtpSoftAtHome(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    manufact_re = re.compile(
        "^220---------- Welcome to SoftAtHome FTP Server",
        re.IGNORECASE
    )

    tests = {
        "FtpSoftAtHome_1": {
            "global_metadata": {
                "manufacturer": Manufacturer.SOFT_AT_HOME,
            },
            "local_metadata": {
                "product": "SoftAtHome Framework"
            }
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.manufact_re.search(banner):
            meta.global_metadata.manufacturer = Manufacturer.SOFT_AT_HOME
            meta.local_metadata.product = "SoftAtHome Framework"

        return meta

    """ Tests
    "220---------- Welcome to SoftAtHome FTP Server  [privsep]  ---------\r\n220-You are user number 1 of 32 allowed.\r\n220-Local time is now 00:31. Server port: 21.\r\n220-This is a private system - No anonymous login\r\n220-IPv6 connections are also welcome on this server.\r\n220 You will be disconnected after 10 minutes of inactivity.\r\n"
    "220---------- Welcome to SoftAtHome FTP Server  [privsep]  ---------\r\n220-You are user number 1 of 32 allowed.\r\n220-Local time is now 00:31. Server port: 21.\r\n220-This is a private system - No anonymous login\r\n220-IPv6 connections are also welcome on this server.\r\n220 You will be disconnected after 10 minutes of inactivity.\r\n"
    "220---------- Welcome to SoftAtHome FTP Server  [privsep]  ---------\r\n220-You are user number 1 of 32 allowed.\r\n220-Local time is now 00:32. Server port: 21.\r\n220-This is a private system - No anonymous login\r\n220-IPv6 connections are also welcome on this server.\r\n220 You will be disconnected after 10 minutes of inactivity.\r\n"
    "220---------- Welcome to SoftAtHome FTP Server  [privsep]  ---------\r\n220-You are user number 1 of 32 allowed.\r\n220-Local time is now 01:33. Server port: 21.\r\n220-This is a private system - No anonymous login\r\n220-IPv6 connections are also welcome on this server.\r\n220 You will be disconnected after 10 minutes of inactivity.\r\n"
    "220---------- Welcome to SoftAtHome FTP Server  [privsep]  ---------\r\n220-You are user number 1 of 32 allowed.\r\n220-Local time is now 00:34. Server port: 21.\r\n220-This is a private system - No anonymous login\r\n220-IPv6 connections are also welcome on this server.\r\n220 You will be disconnected after 10 minutes of inactivity.\r\n"
    "220---------- Welcome to SoftAtHome FTP Server  [privsep]  ---------\r\n220-You are user number 1 of 32 allowed.\r\n220-Local time is now 00:34. Server port: 21.\r\n220-This is a private system - No anonymous login\r\n220-IPv6 connections are also welcome on this server.\r\n220 You will be disconnected after 10 minutes of inactivity.\r\n"
    "220---------- Welcome to SoftAtHome FTP Server  [privsep]  ---------\r\n220-You are user number 1 of 32 allowed.\r\n220-Local time is now 00:35. Server port: 21.\r\n220-This is a private system - No anonymous login\r\n220-IPv6 connections are also welcome on this server.\r\n220 You will be disconnected after 10 minutes of inactivity.\r\n"
    """
