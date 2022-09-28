from abc import ABCMeta, abstractmethod
from convexus.sdkcore.entities.currency import Token
from convexus.sdk.constants import FeeAmount

class PoolFactoryProvider(metaclass=ABCMeta):
  """
  * Provides information about a pool factory
  """

  @abstractmethod
  def getPool (
    self,
    tokenA: Token,
    tokenB: Token,
    fee: FeeAmount
  ) -> str:
    """
     * Return the pool address given pool tokens and fees
     * @param tokenA First token
     * @param tokenB Second token
     * @param fee The pool fee
    """
    pass

class NoPoolFactoryProvider(PoolFactoryProvider):
  """
  * This pool factory provider does not know how to fetch any pool factory data. 
  * It throws whenever it is required. Useful if you
  * do not need to load factory data for your use case.
  """

  ERROR_MESSAGE = 'No pool factory provider was given'
  
  def getPool (
    self,
    _tokenA: Token,
    _tokenB: Token,
    _fee: FeeAmount
  ) -> str:
    raise Exception(NoPoolFactoryProvider.ERROR_MESSAGE)