from convexus.sdkcore.entities.currency import Currency, NativeCurrency, Token

class Icx(NativeCurrency):
  """
  * ICX is the main usage of a 'native' currency, i.e. for ICON mainnet and all testnets
  """

  wrappedAddress: str = 'cx1111111111111111111111111111111111111111'

  def __init__(self):
    super().__init__(18, 'ICX', 'ICX')

  @property
  def wrapped (self) -> Token:
    return Token(Icx.wrappedAddress, 18, 'ICX', 'ICX')

  def equals(self, other: Currency) -> bool:
    return other.isNative and other.symbol == self.symbol
  
  @staticmethod
  def isWrappedAddress (address: str) -> bool:
    return Icx.wrappedAddress == address
  

