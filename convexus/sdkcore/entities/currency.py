import asyncio
from abc import ABCMeta, abstractmethod
from typing import Union
from convexus.icontoolkit.validateAndParseAddress import validateAndParseAddress
from convexus.icontoolkit.contract import Contract

class BaseCurrency(metaclass=ABCMeta):
  """
  * A currency is any fungible financial instrument, including ICX, all IRC2 tokens, and other chain-native currencies
  """

  @property
  @abstractmethod
  def isNative(self) -> bool:
    """
    * Returns whether the currency is native to the chain and must be wrapped (e.g. ICX)
    """
    pass

  @property
  @abstractmethod
  def isToken(self) -> bool:
    """
    * Returns whether the currency is a token that is usable in Convexus without wrapping
    """
    pass

  def __init__(self, decimals: int, symbol: str = None, name: str = None):
    """
    * Constructs an instance of the base class `BaseCurrency`.
    * @param decimals decimals of the currency
    * @param symbol symbol of the currency
    * @param name of the currency
    """
    assert decimals >= 0 and decimals < 255 and isinstance(decimals, int), 'DECIMALS'

    """
    * The decimals used in representing currency amounts
    """
    self.decimals = decimals

    """
    * The symbol of the currency, i.e. a short textual non-unique identifier
    """
    self.symbol = symbol

    """
    * The name of the currency, i.e. a descriptive textual non-unique identifier
    """
    self.name = name

  @abstractmethod
  def equals(self, other: 'Currency') -> bool:
    """
    * Returns whether this currency is functionally equivalent to the other currency
    * @param other the other currency
    """
    pass

  def __eq__(self, __o) -> bool:
    return self.equals(__o)

  @property
  @abstractmethod
  def wrapped(self) -> 'Token':
    """
    * Return the wrapped version of this currency that can be used with the Convexus contracts. Currencies must
    * implement this to be used in Convexus
    """
    pass

class NativeCurrency (BaseCurrency, metaclass=ABCMeta):
  """
  * Represents the native currency of the chain on which it resides, e.g.
  """
  
  @property
  def isNative(self) -> bool:
    return True

  @property
  def isToken(self) -> bool:
    return False

  @property
  def address(self) -> None:
    return None


class Token(BaseCurrency, metaclass=ABCMeta):
  """
  * Represents an IRC2 token with a unique address and some metadata.
  """

  @property
  def isNative(self) -> bool:
    return False

  @property
  def isToken(self) -> bool:
    return True

  @staticmethod
  async def fromContract (contract: Contract) -> 'Token':
    if Icx.isWrappedAddress(contract.address):
      return Icx().wrapped

    decimals, name, symbol = await asyncio.gather(
      contract.decimals(), 
      contract.name(), 
      contract.symbol()
    )
    return Token(contract.address, decimals, symbol, name)

  def __init__(self, address: str, decimals: int, symbol: str = None, name: str = None):
    super().__init__(decimals, symbol, name)
    
    """
    * The contract address on the chain on which this token lives
    """
    self.address = validateAndParseAddress(address)

  def __repr__(self) -> str:
    return str(self.__dict__)

  def equals(self, other: 'Currency') -> bool:
    """
    * Returns true if the two tokens are equivalent, i.e. have the same address.
    * @param other other token to compare
    """
    return other.isToken and self.address == other.address

  def sortsBefore(self, other: 'Token') -> bool:
    """
    * Returns true if the address of this token sorts before the address of the other token
    * @param other other token to compare
    * @throws if the tokens have the same address
    * @throws if the tokens are on different chains
    """
    assert self.address != other.address, 'ADDRESSES'
    return self.address.lower() < other.address.lower()

  @property
  def wrapped(self) -> 'Token':
    """
    * Return this token, which does not need to be wrapped
    """
    return self
  
Currency = Union[NativeCurrency, Token]


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
  

