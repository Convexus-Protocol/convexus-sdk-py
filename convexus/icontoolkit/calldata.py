from convexus.icontoolkit.constants import BigintIsh
from convexus.icontoolkit.BigInt import BigInt

def toHex (bigintIsh: BigintIsh):
  """
  * Converts a bigintish to a hex string
  * @param bigintIsh
  * @returns The hex encoded calldata
  """
  bigInt = BigInt(bigintIsh)
  return hex(bigInt)