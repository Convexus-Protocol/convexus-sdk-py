from typing import List
from icontoolkit.calldata import toHex
from icontoolkit.interface import Interface, CallData
from sdk.entities.pool import Pool

from sdk.artifacts.contracts.PoolInitializer.PoolInitializer import IPoolInitializer

class PoolInitializer:
  INTERFACE: Interface = Interface(IPoolInitializer, "PoolInitializer")

  @staticmethod
  def setContractAddress (contractAddress: str):
    PoolInitializer.INTERFACE = Interface(IPoolInitializer, contractAddress)

  @staticmethod
  def encodeCreate(pool: Pool) -> CallData:
    return PoolInitializer.INTERFACE.encodeFunctionData('createAndInitializePoolIfNecessary', [
      pool.token0.address,
      pool.token1.address,
      pool.fee,
      toHex(pool.sqrtRatioX96)
    ])

  @staticmethod
  def createCallParameters(pool: Pool) -> List[CallData]:
    return [PoolInitializer.encodeCreate(pool)]
