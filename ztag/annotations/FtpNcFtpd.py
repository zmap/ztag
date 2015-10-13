import re
from ztag.annotation import Annotation
from ztag import protocols
import ztag.test


class FtpNcFtpd(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    impl_re = re.compile(
        "NcFTPd Server \(licensed copy\) ready",
        re.IGNORECASE
    )

    def process(self, obj, meta):
        banner = obj["banner"]

        if impl_re.search(banner):
            meta.local_metadata.product = "NcFTPD"

        return meta

    """ Tests
    "220 ftp522.pair.com NcFTPd Server (licensed copy) ready.\r\n"
    "220 holodeck.cloudnet.com NcFTPd Server (licensed copy) ready.\r\n"
    "220-russams.webair.com NcFTPd Server (licensed copy) ready.\r\n220-\r\n220-This computer system is for authorized users only. All activity is logged and\r\n220-regulary checked by systems personal. Individuals using this system without\r\n220-authority or in excess of their authority are subject to having all their\r\n220-services revoked. Any illegal services run by user or attempts to take down\r\n220-this server or its services will be reported to local law enforcement, and\r\n220-said user will be punished to the full extent of the law. Anyone using this\r\n220-system consents to these terms.\r\n220-\r\n220 \r\n"
    "220 ftp520.pair.com NcFTPd Server (licensed copy) ready.\r\n"
    "220 ftp531.pair.com NcFTPd Server (licensed copy) ready.\r\n"
    "220 www1.g6.pair.com NcFTPd Server (licensed copy) ready.\r\n"
    "220 ftp548.pair.com NcFTPd Server (licensed copy) ready.\r\n"
    "220 ftp544.pair.com NcFTPd Server (licensed copy) ready.\r\n"
    "220 www1.g3.pair.com NcFTPd Server (licensed copy) ready.\r\n"
    "220 ftp244.pair.com NcFTPd Server (licensed copy) ready.\r\n"
    "220 ftp528.pair.com NcFTPd Server (licensed copy) ready.\r\n"
    "220 ftp449.pair.com NcFTPd Server (licensed copy) ready.\r\n"
    "220 qs2741.pair.com NcFTPd Server (licensed copy) ready.\r\n"
    "220 ftp557.pair.com NcFTPd Server (licensed copy) ready.\r\n"
    "220-ftp.datarealm.com NcFTPd Server (licensed copy) ready.\r\n220-\r\n220-Welcome to DataRealm Internet Services!\r\n220-\r\n220-\r\n220 \r\n"
    "220 ftp.womenslifestylemagazine.com NcFTPd Server (licensed copy) ready.\r\n"
    "220 ftp112.pair.com NcFTPd Server (licensed copy) ready.\r\n"
    "220 www6.g1.pair.com NcFTPd Server (licensed copy) ready.\r\n"
    "220 ftp557.pair.com NcFTPd Server (licensed copy) ready.\r\n"
    "220-davt.webair.com NcFTPd Server (licensed copy) ready.\r\n220-\r\n220-This computer system is for authorized users only. All activity is logged and\r\n220-regulary checked by systems personal. Individuals using this system without\r\n220-authority or in excess of their authority are subject to having all their\r\n220-services revoked. Any illegal services run by user or attempts to take down\r\n220-this server or its services will be reported to local law enforcement, and\r\n220-said user will be punished to the full extent of the law. Anyone using this\r\n220-system consents to these terms.\r\n220-\r\n220 \r\n"
    "220 ftp552.pair.com NcFTPd Server (licensed copy) ready.\r\n"
    """
