from typing import List
from convexus.icontoolkit.BigInt import BigInt
from convexus.icontoolkit.calldata import toHex
from convexus.icontoolkit.constants import BigintIsh
from convexus.icontoolkit.interface import Interface, CallData
from convexus.icontoolkit.validateAndParseAddress import validateAndParseAddress
from convexus.sdk.entities.pool import Pool

from convexus.sdk.artifacts.contracts.PoolInitializer import IPoolInitializer
from convexus.sdk.entities.position import Position
from convexus.sdk.nonfungiblePositionManager import MintOptions, NonfungiblePositionManager
from convexus.sdk.utils.encodeSqrtRatioX96 import encodeSqrtRatioX96
from convexus.sdk.utils.tickMath import TickMath
from convexus.sdkcore import Token
from convexus.sdkcore.entities.currency import Icx
from convexus.sdkcore.entities.fractions.price import Price

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
  def encodeDeposit (token: Token, amount: BigintIsh) -> CallData:
    amount = BigInt(amount)

    if (Icx.isWrappedAddress(token.address)):
      return PoolInitializer.INTERFACE.encodeFunctionDataPayable(
        amount,
        'depositIcx', []
      )
    else:
      return PoolInitializer.INTERFACE.encodeTokenFallbackFunctionData(
        token.address,
        amount,
        'deposit', [], []
      )

  @staticmethod
  def encodeCreateAndMint(
    position: Position,
    recipient: str,
    deadline: int
  ) -> CallData:
    pool = position.pool
    amount0, amount1 = position.mintAmounts
    
    return PoolInitializer.INTERFACE.encodeFunctionData('createAndInitializePoolIfNecessaryAndMintPosition', [
      # For the pool creation+initialization
      pool.token0.address,
      pool.token1.address,
      pool.fee,
      toHex(pool.sqrtRatioX96),
      # For the position minting
      position.tickLower,
      position.tickUpper,
      toHex(amount0),
      toHex(amount1),
      # Slippage shouldn't be an issue as we're creating the pool + mint in a single transaction
      toHex(0),
      toHex(0),
      validateAndParseAddress(recipient),
      toHex(deadline)
    ])

  @staticmethod
  def createCallParameters(pool: Pool) -> List[CallData]:
    return [PoolInitializer.encodeCreate(pool)]

  @staticmethod
  def createAndMintCallParameters(
    position: Position,
    recipient: str,
    deadline: int
  ) -> List[CallData]:
    return [
      PoolInitializer.encodeDeposit(position.pool.token0, position.amount0.quotient),
      PoolInitializer.encodeDeposit(position.pool.token1, position.amount1.quotient),
      PoolInitializer.encodeCreateAndMint(position, recipient, deadline)
    ]
