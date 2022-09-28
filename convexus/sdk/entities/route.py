from dataclasses import dataclass
from typing import List, cast

from convexus.sdk.entities.pool import Pool
from convexus.sdkcore.entities.currency import Currency, Token
from convexus.sdkcore.entities.fractions.price import Price

from functools import reduce

class Route:
  """
  * Represents a list of pools through which a swap can occur
  * @template Currency The input token
  * @template Currency The output token
  """

  def __init__(self, pools: List[Pool], input: Currency, output: Currency):
    """
    * Creates an instance of route.
    * @param pools An array of `Pool` objects, ordered by the route the swap will take
    * @param input The input token
    * @param output The output token
    """
    
    self.pools: List[Pool]
    self.tokenPath: List[Token]
    self.input: Currency
    self.output: Currency
    self.__midPrice: Price | None = None

    assert len(pools) > 0, 'POOLS'

    wrappedInput = input.wrapped
    assert pools[0].involvesToken(wrappedInput), 'INPUT'
    assert pools[len(pools) - 1].involvesToken(output.wrapped), 'OUTPUT'

    # Normalizes token0-token1 order and selects the next token/fee step to add to the path
    tokenPath: List[Token] = [wrappedInput]
    for i, pool in enumerate(pools):
      currentInputToken = tokenPath[i]
      assert currentInputToken.equals(pool.token0) or currentInputToken.equals(pool.token1), 'PATH'
      nextToken = pool.token1 if currentInputToken.equals(pool.token0) else pool.token0
      tokenPath.append(nextToken)

    self.pools = pools
    self.tokenPath = tokenPath
    self.input = input
    self.output = output if output else tokenPath[len(tokenPath) - 1]

  def __repr__(self) -> str:
    return str(self.__dict__)

  """
   * Returns the mid price of the route
  """
  @property
  def midPrice(self) -> Price:
    if (self.__midPrice != None):
      return cast(Price, self.__midPrice)
    
    @dataclass
    class NextInputPrice:
      nextInput: Token
      price: Price

    price = reduce (
      lambda nip, pool:
        NextInputPrice (
          pool.token1,
          nip.price.multiply(pool.token0Price)
        ) if nip.nextInput.equals(pool.token0) else NextInputPrice (
          pool.token0,
          nip.price.multiply(pool.token1Price)
        ),

      self.pools[1:],

      NextInputPrice (
        self.pools[0].token1,
        self.pools[0].token0Price
      ) if self.pools[0].token0.equals(self.input.wrapped) else NextInputPrice (
        self.pools[0].token0,
        self.pools[0].token1Price
      )
    ).price

    self.__midPrice = Price(self.input, self.output, price.denominator, price.numerator)
    return self.__midPrice
