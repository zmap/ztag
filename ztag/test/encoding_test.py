from ztag.transform import ZMapTransform
import unittest


class CleanBannerTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_clean_banner(self):
        # Note -- regexes don't check for word boundaries, so it will hit matching substrings that
        # actually correspond to different hosts.
        cases_format = {
            # Typical hostname
            "Received connection from researchscan{worker}.eecs.umich.edu on port 1234":
                "Received connection from CLIENT_HOSTNAME on port 1234",
            # Close to scanner hostname
            "Received connection from otherscan{worker}.eecs.umich.edu on port 1234": False,
            # Typical IP
            "Received connection from 141.212.{ip3}.{ip4} on port 1234":
                "Received connection from CLIENT_IP on port 1234",
            # Close to scanner IP
            "Received connection from 141.212.123.{ip4} on port 1234": False,
            "Received connection from 141.213.122.{ip4} on port 1234": False,
            "Received connection from 142.212.122.{ip4} on port 1234": False,
            # Bad IP separator
            "Received connection from 141,212,{ip3},{ip4} on port 1234": False,
            # SFJ: Typical hostname
            "Received connection from worker-{worker}.sfj.corp.censys.io on port 1234":
                "Received connection from CLIENT_HOSTNAME on port 1234",
            # SFJ: Close to scanner hostname
            "Received connection from manager-{worker}.sfj.corp.censys.io": False,
            # SFJ: Typical IP
            "Received connection from 198.108.66.{ip4} on port 1234":
                "Received connection from CLIENT_IP on port 1234",
            # Both IP and host
            ("Got connection from 141.212.{ip3}.{ip4}:1234 "
             "(researchscan{worker}.eecs.umich.edu:1234)"):
                "Got connection from CLIENT_IP:1234 (CLIENT_HOSTNAME:1234)",
            # IP at end
            "Got connection from 141.212.{ip3}.{ip4}": "Got connection from CLIENT_IP",
            # IP at start
            "141.212.{ip3}.{ip4} connected.": "CLIENT_IP connected.",
            # Host at end
            "Got connection from researchscan{worker}.eecs.umich.edu":
                "Got connection from CLIENT_HOSTNAME",
            # Host at start
            "researchscan{worker}.eecs.umich.edu connected": "CLIENT_HOSTNAME connected",
            # Isolated IP
            "141.212.{ip3}.{ip4}": "CLIENT_IP",
            # Isolated host
            "researchscan{worker}.eecs.umich.edu": "CLIENT_HOSTNAME",
            # IP appears twice
            "Got connection from 141.212.{ip3}.{ip4}, rejecting 141.212.{ip3}.{ip4}.":
                "Got connection from CLIENT_IP, rejecting CLIENT_IP.",
            # Host appears twice
            ("Got connection from researchscan{worker}.eecs.umich.edu, "
             "rejecting researchscan{worker}.eecs.umich.edu."):
                "Got connection from CLIENT_HOSTNAME, rejecting CLIENT_HOSTNAME.",
            # IP appears twice on different lines
            "Got connection from 141.212.{ip3}.{ip4}\nrejecting 141.212.{ip3}.{ip4}.":
                "Got connection from CLIENT_IP\nrejecting CLIENT_IP.",
            # Host appears twice on different lines
            ("Got connection from researchscan{worker}.eecs.umich.edu\n"
             "rejecting researchscan{worker}.eecs.umich.edu."):
                "Got connection from CLIENT_HOSTNAME\nrejecting CLIENT_HOSTNAME.",
            # SFJ: Both IP and host
            "Got connection from 198.108.66.{ip4}:1234 (worker-{worker}.sfj.corp.censys.io:1234)":
                "Got connection from CLIENT_IP:1234 (CLIENT_HOSTNAME:1234)",
            # SFJ: IP at end
            "Got connection from 198.108.66.{ip4}": "Got connection from CLIENT_IP",
            # SFJ: IP at start
            "198.108.66.{ip4} connected.": "CLIENT_IP connected.",
            # SFJ: Host at end
            "Got connection from worker-{worker}.sfj.corp.censys.io":
                "Got connection from CLIENT_HOSTNAME",
            # SFJ: Host at start
            "worker-{worker}.sfj.corp.censys.io connected.": "CLIENT_HOSTNAME connected.",
            # SFJ: Isolated IP
            "198.108.66.{ip4}": "CLIENT_IP",
            # SFJ: Isolated host
            "worker-{worker}.sfj.corp.censys.io": "CLIENT_HOSTNAME",
            # SFJ: IP appears twice
            "Got connection from 198.108.66.{ip4}, rejecting 198.108.66.{ip4}.":
                "Got connection from CLIENT_IP, rejecting CLIENT_IP.",
            # SFJ: Host appears twice
            "Got connection from worker-{worker}.sfj.corp.censys.io, "
                "rejecting worker-{worker}.sfj.corp.censys.io.":
                "Got connection from CLIENT_HOSTNAME, rejecting CLIENT_HOSTNAME.",
            # SFJ: IP appears twice on different lines
            "Got connection from 198.108.66.{ip4}\nrejecting 198.108.66.{ip4}.":
                "Got connection from CLIENT_IP\nrejecting CLIENT_IP.",
            # SFJ: Host appears twice on different lines
            ("Got connection from worker-{worker}.sfj.corp.censys.io\n"
             "rejecting worker-{worker}.sfj.corp.censys.io."):
                "Got connection from CLIENT_HOSTNAME\nrejecting CLIENT_HOSTNAME."

        }
        cases = {}
        for k, v in cases_format.items():
            if not v:
                v = k
            for ip3 in (121, 122):
                for ip4 in range(0, 256):
                    for worker in range(1, 10):
                        kk = k.format(worker=worker, ip3=ip3, ip4=ip4)
                        vv = v.format(worker=worker, ip3=ip3, ip4=ip4)
                        cases[kk] = vv

        for test_input, expected in cases.items():
            actual = ZMapTransform.clean_banner(test_input)
            self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
