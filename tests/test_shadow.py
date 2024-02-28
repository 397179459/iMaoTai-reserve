import unittest
from shadow import shadow
class TestShadow(unittest.TestCase):
    def test_shadow(self):
        self.assertEqual(shadow("12345678901"), "123****8901")
        self.assertEqual(shadow("98765403210"), "987****3210")
        self.assertEqual(shadow("11111111111"), "111****1111")
        self.assertEqual(shadow("123456789"), "123***789")
        self.assertEqual(shadow("987654321"), "987***321")

if __name__ == '__main__':
    unittest.main()
