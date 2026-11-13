import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills" / "analizador-web" / "scripts"))
from unittest.mock import patch
from safety import UnsafeTarget, validate_public_url, redact_url


class SafetyTests(unittest.TestCase):
    def test_rejects_non_http_schemes(self):
        with self.assertRaises(UnsafeTarget):
            validate_public_url("file:///etc/passwd")

    def test_rejects_credentials(self):
        with self.assertRaises(UnsafeTarget):
            validate_public_url("https://user:pass@example.com")

    def test_rejects_nonstandard_ports(self):
        with self.assertRaises(UnsafeTarget):
            validate_public_url("https://example.com:8443")

    def test_rejects_localhost(self):
        with self.assertRaises(UnsafeTarget):
            validate_public_url("http://localhost")

    @patch("safety.socket.getaddrinfo")
    def test_rejects_private_dns_result(self, dns):
        dns.return_value=[(2,1,6,"",("192.168.1.10",443))]
        with self.assertRaises(UnsafeTarget):
            validate_public_url("https://private.example")

    @patch("safety.socket.getaddrinfo")
    def test_accepts_public_dns_result(self, dns):
        dns.return_value=[(2,1,6,"",("93.184.216.34",443))]
        self.assertEqual(validate_public_url("https://example.com"),"https://example.com/")

    def test_redacts_query_and_fragment(self):
        self.assertEqual(redact_url("https://example.com/a?token=secret#x"),"https://example.com/a")


if __name__=="__main__": unittest.main()
