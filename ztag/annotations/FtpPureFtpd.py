import re
from ztag.annotation import Annotation
from ztag import protocols
import ztag.test


class FtpPureFptd(Annotation):
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    def process(self, obj, meta):
        banner = obj["banner"]

        if (
            banner.startswith(
                "220---------- \\xbb\\xb6\\xd3\\xad\\xc0\\xb4\\xb5\\xbd Pure-FTPd") or
            banner.startswith("220---------- Bienvenue sur Pure-FTPd") or
            banner.startswith("220---------- Welcome to Pure-FTPd")
        ):
            meta.local_metadata.product = "Pure-FTPd"

        return meta

    """ Tests
    "220---------- Welcome to Pure-FTPd [privsep] [TLS] ----------\r\n220-You are user number 1 of 50 allowed.\r\n220-Local time is now 19:29. Server port: 21.\r\n220-IPv6 connections are also welcome on this server.\r\n220 You will be disconnected after 15 minutes of inactivity.\r\n"
    "220---------- Welcome to Pure-FTPd [privsep] [TLS] ----------\r\n220-You are user number 2 of 10 allowed.\r\n220-Local time is now 18:29. Server port: 21.\r\n220-This is a private system - No anonymous login\r\n220-IPv6 connections are also welcome on this server.\r\n220 You will be disconnected after 15 minutes of inactivity.\r\n"
    "220---------- Welcome to Pure-FTPd [privsep] [TLS] ----------\r\n220-You are user number 1 of 50 allowed.\r\n220-Local time is now 17:29. Server port: 21.\r\n220-This is a private system - No anonymous login\r\n220-IPv6 connections are also welcome on this server.\r\n220 You will be disconnected after 15 minutes of inactivity.\r\n"
    "220---------- Welcome to Pure-FTPd [privsep] [TLS] ----------\r\n220-You are user number 1 of 50 allowed.\r\n220-Local time is now 18:29. Server port: 21.\r\n220-This is a private system - No anonymous login\r\n220-IPv6 connections are also welcome on this server.\r\n220 You will be disconnected after 15 minutes of inactivity.\r\n"
    "220---------- Welcome to Pure-FTPd [privsep] [TLS] ----------\r\n220-You are user number 1 of 50 allowed.\r\n220-Local time is now 01:29. Server port: 21.\r\n220-This is a private system - No anonymous login\r\n220-IPv6 connections are also welcome on this server.\r\n220 You will be disconnected after 15 minutes of inactivity.\r\n"
    "220---------- Welcome to Pure-FTPd [privsep] [TLS] ----------\r\n220-You are user number 3 of 500 allowed.\r\n220-Local time is now 20:29. Server port: 21.\r\n220-This is a private system - No anonymous login\r\n220 You will be disconnected after 15 minutes of inactivity.\r\n"
    "220---------- Welcome to Pure-FTPd [privsep] [TLS] ----------\r\n220-You are user number 1 of 50 allowed.\r\n220-Local time is now 18:31. Server port: 21.\r\n220-IPv6 connections are also welcome on this server.\r\n220 You will be disconnected after 15 minutes of inactivity.\r\n"
    "220---------- Bienvenue sur Pure-FTPd [privsep] [TLS] ----------\r\n220-Vous etes l'utilisateur 1 sur les 100 autorises.\r\n220-L'heure locale est 01:36. Port du serveur : 21.\r\n220-Ceci est un systeme prive - Aucun utilisateur anonyme autorise\r\n220-Les connections en IPv6 sont les bienvenues sur ce serveur.\r\n220 Vous serez deconnectes apres 5 minutes d'inactivite.\r\n"
    "220---------- Bienvenue sur Pure-FTPd [privsep] [TLS] ----------\r\n220-Vous etes l'utilisateur 1 sur les 100 autorises.\r\n220-L'heure locale est 01:32. Port du serveur : 21.\r\n220-Ceci est un systeme prive - Aucun utilisateur anonyme autorise\r\n220-Les connections en IPv6 sont les bienvenues sur ce serveur.\r\n220 Vous serez deconnectes apres 5 minutes d'inactivite.\r\n"
    "220---------- \\xbb\\xb6\\xd3\\xad\\xc0\\xb4\\xb5\\xbd Pure-FTPd [privsep] ----------\r\n220-\\xc4\\xfa\\xca\\xc7\\xb5\\xda 1 \\xb8\\xf6\\xca\\xb9\\xd3\\xc3\\xd5\\xdf\\xa3\\xac\\xd7\\xee\\xb6\\xe0\\xbf\\xc9\\xb4\\xef 50 \\xb8\\xf6\\xc1\\xac\\xbd\\xd3\r\n220-\\xcf\\xd6\\xd4\\xda\\xb1\\xbe\\xb5\\xd8\\xca\\xb1\\xbc\\xe4\\xca\\xc7 07:31\\xa1\\xa3\\xb7\\xfe\\xce\\xf1\\xc6\\xf7\\xb6\\xcb\\xbf\\xda\\xa3\\xba 21\\xa1\\xa3\r\n220-\\xd5\\xe2\\xca\\xc7\\xcb\\xbd\\xc8\\xcb\\xcf\\xb5\\xcd\\xb3 - \\xb2\\xbb\\xbf\\xaa\\xb7\\xc5\\xc4\\xe4\\xc3\\xfb\\xb5\\xc7\\xc2\\xbc\r\n220-\\xd5\\xe2\\xb2\\xbf\\xd6\\xf7\\xbb\\xfa\\xd2\\xb2\\xbb\\xb6\\xd3\\xadIPv6\\xb5\\xc4\\xc1\\xac\\xbd\\xd3\r\n220 \\xd4\\xda 15 \\xb7\\xd6\\xd6\\xd3\\xc4\\xda\\xc3\\xbb\\xd3\\xd0\\xbb\\xee\\xb6\\xaf\\xa3\\xac\\xc4\\xfa\\xb1\\xbb\\xbb\\xe1\\xb6\\xcf\\xcf\\xdf\\xa1\\xa3\r\n"
    "220---------- \\xbb\\xb6\\xd3\\xad\\xc0\\xb4\\xb5\\xbd Pure-FTPd [privsep] ----------\r\n220-\\xc4\\xfa\\xca\\xc7\\xb5\\xda 3 \\xb8\\xf6\\xca\\xb9\\xd3\\xc3\\xd5\\xdf\\xa3\\xac\\xd7\\xee\\xb6\\xe0\\xbf\\xc9\\xb4\\xef 50 \\xb8\\xf6\\xc1\\xac\\xbd\\xd3\r\n220-\\xcf\\xd6\\xd4\\xda\\xb1\\xbe\\xb5\\xd8\\xca\\xb1\\xbc\\xe4\\xca\\xc7 07:30\\xa1\\xa3\\xb7\\xfe\\xce\\xf1\\xc6\\xf7\\xb6\\xcb\\xbf\\xda\\xa3\\xba 21\\xa1\\xa3\r\n220-\\xd5\\xe2\\xca\\xc7\\xcb\\xbd\\xc8\\xcb\\xcf\\xb5\\xcd\\xb3 - \\xb2\\xbb\\xbf\\xaa\\xb7\\xc5\\xc4\\xe4\\xc3\\xfb\\xb5\\xc7\\xc2\\xbc\r\n220-\\xd5\\xe2\\xb2\\xbf\\xd6\\xf7\\xbb\\xfa\\xd2\\xb2\\xbb\\xb6\\xd3\\xadIPv6\\xb5\\xc4\\xc1\\xac\\xbd\\xd3\r\n220 \\xd4\\xda 15 \\xb7\\xd6\\xd6\\xd3\\xc4\\xda\\xc3\\xbb\\xd3\\xd0\\xbb\\xee\\xb6\\xaf\\xa3\\xac\\xc4\\xfa\\xb1\\xbb\\xbb\\xe1\\xb6\\xcf\\xcf\\xdf\\xa1\\xa3\r\n"
    "220---------- Welcome to Pure-FTPd [privsep] [TLS] ----------\r\n220-You are user number 1 of 50 allowed.\r\n220-Local time is now 02:31. Server port: 21.\r\n220-This is a private system - No anonymous login\r\n220-IPv6 connections are also welcome on this server.\r\n220 You will be disconnected after 15 minutes of inactivity.\r\n"
    "220---------- \\xbb\\xb6\\xd3\\xad\\xc0\\xb4\\xb5\\xbd Pure-FTPd [privsep] ----------\r\n220-\\xc4\\xfa\\xca\\xc7\\xb5\\xda 1 \\xb8\\xf6\\xca\\xb9\\xd3\\xc3\\xd5\\xdf\\xa3\\xac\\xd7\\xee\\xb6\\xe0\\xbf\\xc9\\xb4\\xef 50 \\xb8\\xf6\\xc1\\xac\\xbd\\xd3\r\n220-\\xcf\\xd6\\xd4\\xda\\xb1\\xbe\\xb5\\xd8\\xca\\xb1\\xbc\\xe4\\xca\\xc7 17:21\\xa1\\xa3\\xb7\\xfe\\xce\\xf1\\xc6\\xf7\\xb6\\xcb\\xbf\\xda\\xa3\\xba 21\\xa1\\xa3\r\n220-\\xd5\\xe2\\xca\\xc7\\xcb\\xbd\\xc8\\xcb\\xcf\\xb5\\xcd\\xb3 - \\xb2\\xbb\\xbf\\xaa\\xb7\\xc5\\xc4\\xe4\\xc3\\xfb\\xb5\\xc7\\xc2\\xbc\r\n220-\\xd5\\xe2\\xb2\\xbf\\xd6\\xf7\\xbb\\xfa\\xd2\\xb2\\xbb\\xb6\\xd3\\xadIPv6\\xb5\\xc4\\xc1\\xac\\xbd\\xd3\r\n220 \\xd4\\xda 15 \\xb7\\xd6\\xd6\\xd3\\xc4\\xda\\xc3\\xbb\\xd3\\xd0\\xbb\\xee\\xb6\\xaf\\xa3\\xac\\xc4\\xfa\\xb1\\xbb\\xbb\\xe1\\xb6\\xcf\\xcf\\xdf\\xa1\\xa3\r\n"
    "220---------- \\xbb\\xb6\\xd3\\xad\\xc0\\xb4\\xb5\\xbd Pure-FTPd [privsep] ----------\r\n220-\\xc4\\xfa\\xca\\xc7\\xb5\\xda 1 \\xb8\\xf6\\xca\\xb9\\xd3\\xc3\\xd5\\xdf\\xa3\\xac\\xd7\\xee\\xb6\\xe0\\xbf\\xc9\\xb4\\xef 50 \\xb8\\xf6\\xc1\\xac\\xbd\\xd3\r\n220-\\xcf\\xd6\\xd4\\xda\\xb1\\xbe\\xb5\\xd8\\xca\\xb1\\xbc\\xe4\\xca\\xc7 07:25\\xa1\\xa3\\xb7\\xfe\\xce\\xf1\\xc6\\xf7\\xb6\\xcb\\xbf\\xda\\xa3\\xba 21\\xa1\\xa3\r\n220-\\xd5\\xe2\\xca\\xc7\\xcb\\xbd\\xc8\\xcb\\xcf\\xb5\\xcd\\xb3 - \\xb2\\xbb\\xbf\\xaa\\xb7\\xc5\\xc4\\xe4\\xc3\\xfb\\xb5\\xc7\\xc2\\xbc\r\n220-\\xd5\\xe2\\xb2\\xbf\\xd6\\xf7\\xbb\\xfa\\xd2\\xb2\\xbb\\xb6\\xd3\\xadIPv6\\xb5\\xc4\\xc1\\xac\\xbd\\xd3\r\n220 \\xd4\\xda 15 \\xb7\\xd6\\xd6\\xd3\\xc4\\xda\\xc3\\xbb\\xd3\\xd0\\xbb\\xee\\xb6\\xaf\\xa3\\xac\\xc4\\xfa\\xb1\\xbb\\xbb\\xe1\\xb6\\xcf\\xcf\\xdf\\xa1\\xa3\r\n"
    "220---------- \\xbb\\xb6\\xd3\\xad\\xc0\\xb4\\xb5\\xbd Pure-FTPd [privsep] ----------\r\n220-\\xc4\\xfa\\xca\\xc7\\xb5\\xda 1 \\xb8\\xf6\\xca\\xb9\\xd3\\xc3\\xd5\\xdf\\xa3\\xac\\xd7\\xee\\xb6\\xe0\\xbf\\xc9\\xb4\\xef 50 \\xb8\\xf6\\xc1\\xac\\xbd\\xd3\r\n220-\\xcf\\xd6\\xd4\\xda\\xb1\\xbe\\xb5\\xd8\\xca\\xb1\\xbc\\xe4\\xca\\xc7 07:31\\xa1\\xa3\\xb7\\xfe\\xce\\xf1\\xc6\\xf7\\xb6\\xcb\\xbf\\xda\\xa3\\xba 21\\xa1\\xa3\r\n220-\\xd5\\xe2\\xca\\xc7\\xcb\\xbd\\xc8\\xcb\\xcf\\xb5\\xcd\\xb3 - \\xb2\\xbb\\xbf\\xaa\\xb7\\xc5\\xc4\\xe4\\xc3\\xfb\\xb5\\xc7\\xc2\\xbc\r\n220-\\xd5\\xe2\\xb2\\xbf\\xd6\\xf7\\xbb\\xfa\\xd2\\xb2\\xbb\\xb6\\xd3\\xadIPv6\\xb5\\xc4\\xc1\\xac\\xbd\\xd3\r\n220 \\xd4\\xda 15 \\xb7\\xd6\\xd6\\xd3\\xc4\\xda\\xc3\\xbb\\xd3\\xd0\\xbb\\xee\\xb6\\xaf\\xa3\\xac\\xc4\\xfa\\xb1\\xbb\\xbb\\xe1\\xb6\\xcf\\xcf\\xdf\\xa1\\xa3\r\n"
    """
