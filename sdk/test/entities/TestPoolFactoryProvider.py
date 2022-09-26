from sdk.entities.factoryProvider import PoolFactoryProvider

from sdkcore.entities.currency import Token
from sdk.constants import FeeAmount
import re

class TestPoolFactoryProvider(PoolFactoryProvider):

  # Generate fake contract addresses from a simple checksum 
  # algorithm based on the token addresses
  def checksum (self, s: str):
    chk = 1103515245
    length = len(s)

    for i in range(length):
      chk += ord(s[i]) * (i + 1)

    n = "%x" % (chk & 0xffffffff)
    zeroes = "00000000"
    return zeroes[len(n):] + n

  def getPool (self, tokenA: Token, tokenB: Token, fee: FeeAmount) -> str:
    if (not tokenA.sortsBefore(tokenB)):
      tokenC = tokenA
      tokenA = tokenB
      tokenB = tokenC

    # need 40 characters for contracts: 8 * 5 characters will be enough, so 5 checksums calls
    seed = tokenA.address.replace("cx", "") + tokenB.address.replace("cx", "")
    # get 5 chunks
    chunks = re.findall(r".{1,16}", seed)

    if (chunks != None and len(chunks) == 5):
      return "cx" \
        + self.checksum(str(fee.value) + chunks[0] + seed) \
        + self.checksum(str(fee.value) + chunks[1] + seed) \
        + self.checksum(str(fee.value) + chunks[2] + seed) \
        + self.checksum(str(fee.value) + chunks[3] + seed) \
        + self.checksum(str(fee.value) + chunks[4] + seed)

    raise Exception("Invalid chunks")
  