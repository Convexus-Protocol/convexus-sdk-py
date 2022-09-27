import unittest

from convexus.icontoolkit.validateAndParseAddress import validateAndParseAddress

class TestValidateAndParseAddress(unittest.TestCase):

  def test_returnsSameAddress(self):
    self.assertEqual(
      validateAndParseAddress("hx23b9aa06f3a0413c40a91591cb8d28319e05bbb9"), 
      "hx23b9aa06f3a0413c40a91591cb8d28319e05bbb9")

  def test_returnsAddressIfSpaces(self):
    self.assertEqual(
      validateAndParseAddress("  hx23b9aa06f3a0413c40a91591cb8d28319e05bbb9  "), 
      "hx23b9aa06f3a0413c40a91591cb8d28319e05bbb9")

  def test_throwsIfNotValid(self):
    with self.assertRaises(Exception):
      validateAndParseAddress("0x23b9aa06f3a0413c40a91591cb8d28319e05bbb9")

if __name__ == '__main__':
    unittest.main()