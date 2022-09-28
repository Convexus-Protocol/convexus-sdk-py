from abc import ABCMeta
from dataclasses import dataclass
from typing import List, Union, cast
from convexus.icontoolkit.BigInt import BigInt
from convexus.icontoolkit.calldata import toHex

from convexus.icontoolkit.constants import BigintIsh
from convexus.icontoolkit.interface import CallData, Interface
from convexus.icontoolkit.validateAndParseAddress import validateAndParseAddress

from convexus.sdkcore.entities.icx import Icx
from convexus.sdkcore.entities.fractions.percent import Percent
from convexus.sdkcore.entities.fractions.currencyAmount import CurrencyAmount
from convexus.sdkcore.entities.currency import NativeCurrency, Token

from convexus.sdk.entities.position import Position, PositionConstructorArgs
from convexus.sdk.artifacts.contracts.NonfungiblePositionManager import INonfungiblePositionManager

MaxUint128 = toHex((2**128) - 1)

@dataclass
class MintSpecificOptions:
  """
   * The account that should receive the minted NFT.
  """
  recipient: str

@dataclass
class IncreaseSpecificOptions:
  """
   * Indicates the ID of the position to increase liquidity for.
  """
  tokenId: BigintIsh


@dataclass
class CommonAddLiquidityOptions:
  """
  * Options for producing the calldata to add liquidity.
  """

  """
   * How much the pool price is allowed to move.
  """
  slippageTolerance: Percent

  """
   * When the transaction expires, in epoch seconds.
  """
  deadline: BigintIsh

  """
   * Whether to spend ICX. If true, one of the pool tokens must be WICX, by default false
  """
  useNative: NativeCurrency | None

# CommonAddLiquidityOptions & MintSpecificOptions
@dataclass
class MintOptions:
  """
  * Options for producing the calldata to add liquidity.
  """

  """
   * How much the pool price is allowed to move.
  """
  slippageTolerance: Percent

  """
   * When the transaction expires, in epoch seconds.
  """
  deadline: BigintIsh

  """
   * The account that should receive the minted NFT.
  """
  recipient: str

  """
   * Whether to spend ICX. If true, one of the pool tokens must be WICX, by default false
  """
  useNative: NativeCurrency | None = None
  
# CommonAddLiquidityOptions & IncreaseSpecificOptions
@dataclass
class IncreaseOptions:
  """
  * Options for producing the calldata to add liquidity.
  """

  """
   * How much the pool price is allowed to move.
  """
  slippageTolerance: Percent

  """
   * When the transaction expires, in epoch seconds.
  """
  deadline: BigintIsh

  """
   * Indicates the ID of the position to increase liquidity for.
  """
  tokenId: BigintIsh

  """
   * Whether to spend ICX. If true, one of the pool tokens must be WICX, by default false
  """
  useNative: NativeCurrency | None = None

  
AddLiquidityOptions = Union[MintOptions, IncreaseOptions]

@dataclass
class SafeTransferOptions:
  """
   * The account sending the NFT.
  """
  sender: str

  """
   * The account that should receive the NFT.
  """
  recipient: str

  """
   * The id of the token being sent.
  """
  tokenId: BigintIsh

  """
   * The optional parameter that passes data to the `onERC721Received` call for the staker
  """
  data: str | None = None

# type guard
def isMint(options: AddLiquidityOptions) -> bool:
  return any(map(lambda f: f == 'recipient', options.__dataclass_fields__))

@dataclass
class CollectOptionsNoTokenId:
  """
   * Expected value of tokensOwed0, including as-of-yet-unaccounted-for fees/liquidity value to be burned
  """
  expectedCurrencyOwed0: CurrencyAmount

  """
   * Expected value of tokensOwed1, including as-of-yet-unaccounted-for fees/liquidity value to be burned
  """
  expectedCurrencyOwed1: CurrencyAmount

  """
   * The account that should receive the tokens.
  """
  recipient: str

@dataclass
class CollectOptions:
  """
   * Indicates the ID of the position to collect for.
  """
  tokenId: BigintIsh
  """
   * Expected value of tokensOwed0, including as-of-yet-unaccounted-for fees/liquidity value to be burned
  """
  expectedCurrencyOwed0: CurrencyAmount

  """
   * Expected value of tokensOwed1, including as-of-yet-unaccounted-for fees/liquidity value to be burned
  """
  expectedCurrencyOwed1: CurrencyAmount

  """
   * The account that should receive the tokens.
  """
  recipient: str

@dataclass
class NFTPermitOptions:
  v: int
  r: str
  s: str
  deadline: int
  spender: str

@dataclass
class RemoveLiquidityOptions:
  """
  * Options for producing the calldata to exit a position.
  """

  """
   * The ID of the token to exit
  """
  tokenId: BigintIsh

  """
   * The percentage of position liquidity to exit.
  """
  liquidityPercentage: Percent

  """
   * How much the pool price is allowed to move.
  """
  slippageTolerance: Percent

  """
   * When the transaction expires, in epoch seconds.
  """
  deadline: BigintIsh

  """
   * Parameters to be passed on to collect
  """
  collectOptions: CollectOptionsNoTokenId

  """
   * Whether the NFT should be burned if the entire position is being exited, by default false.
  """
  burnToken: bool | None = None

  """
   * The optional permit of the token ID being exited, in case the exit transaction is being sent by an account that does not own the NFT
  """
  permit: NFTPermitOptions | None = None


class NonfungiblePositionManager(metaclass=ABCMeta):
  INTERFACE: Interface = Interface(INonfungiblePositionManager, "NonfungiblePositionManager")

  @staticmethod
  def setContractAddress (contractAddress: str):
    NonfungiblePositionManager.INTERFACE = Interface(INonfungiblePositionManager, contractAddress)
  
  @staticmethod
  def encodeDeposit (token: Token, amount: BigintIsh) -> CallData:
    amount = BigInt(amount)

    if (Icx.isWrappedAddress(token.address)):
      return NonfungiblePositionManager.INTERFACE.encodeFunctionDataPayable(
        amount,
        'depositIcx', []
      )
    else:
      return NonfungiblePositionManager.INTERFACE.encodeTokenFallbackFunctionData(
        token.address,
        amount,
        'deposit', [], []
      )

  @staticmethod
  def addCallParameters(position: Position, options: AddLiquidityOptions) -> List[CallData]:
    assert position.liquidity > 0, 'ZERO_LIQUIDITY'

    calldatas: List[CallData] = []

    # get amounts
    amounts = position.mintAmounts
    amount0Desired = amounts.amount0
    amount1Desired = amounts.amount1

    # adjust for slippage
    minimumAmounts = position.mintAmountsWithSlippage(options.slippageTolerance)
    amount0Min = toHex(minimumAmounts.amount0)
    amount1Min = toHex(minimumAmounts.amount1)
    deadline = toHex(options.deadline)

    # mint
    if (isMint(options)):
      optionsMint: MintOptions = cast(MintOptions, options)
      recipient: str = validateAndParseAddress(optionsMint.recipient)

      # deposit tokens
      if (amount0Desired > 0):
        calldatas.append(NonfungiblePositionManager.encodeDeposit(position.pool.token0, amount0Desired))
      
      if (amount1Desired > 0):
        calldatas.append(NonfungiblePositionManager.encodeDeposit(position.pool.token1, amount1Desired))

      calldatas.append(
        NonfungiblePositionManager.INTERFACE.encodeFunctionData('mint', [
          [
            position.pool.token0.address,
            position.pool.token1.address,
            position.pool.fee,
            position.tickLower,
            position.tickUpper,
            toHex(amount0Desired),
            toHex(amount1Desired),
            amount0Min,
            amount1Min,
            recipient,
            deadline
          ]
        ])
      )
    else:
      optionsIncrease: IncreaseOptions = cast(IncreaseOptions, options)

      # increase
      # deposit tokens
      if (amount0Desired > 0):
        calldatas.append(NonfungiblePositionManager.encodeDeposit(position.pool.token0, amount0Desired))
      
      if (amount1Desired > 0):
        calldatas.append(NonfungiblePositionManager.encodeDeposit(position.pool.token1, amount1Desired))
      
      calldatas.append(
        NonfungiblePositionManager.INTERFACE.encodeFunctionData('increaseLiquidity', [
          [
            toHex(optionsIncrease.tokenId),
            toHex(amount0Desired),
            toHex(amount1Desired),
            amount0Min,
            amount1Min,
            deadline
          ]
        ])
      )
    
    if (options.useNative):
      wrapped = options.useNative.wrapped
      assert position.pool.token0.equals(wrapped) or position.pool.token1.equals(wrapped), 'NO_WICX'

    return calldatas

  @staticmethod
  def encodeCollect(options: CollectOptions) -> List[CallData]:
    calldatas: List[CallData] = []

    tokenId = toHex(options.tokenId)
    recipient = validateAndParseAddress(options.recipient)

    # collect
    calldatas.append(
      NonfungiblePositionManager.INTERFACE.encodeFunctionData('collect', [
        [
          tokenId,
          recipient,
          MaxUint128,
          MaxUint128
        ]
      ])
    )

    return calldatas
  

  @staticmethod
  def collectCallParameters(options: CollectOptions) -> List[CallData]:
    calldatas: List[CallData] = NonfungiblePositionManager.encodeCollect(options)

    return calldatas
  

  """
   * Produces the calldata for completely or partially exiting a position
   * @param position The position to exit
   * @param options Additional information necessary for generating the calldata
   * @returns The call parameters
  """
  @staticmethod
  def removeCallParameters(position: Position, options: RemoveLiquidityOptions) -> List[CallData]:
    calldatas: List[CallData] = []

    deadline = toHex(options.deadline)
    tokenId = toHex(options.tokenId)

    # construct a partial position with a percentage of liquidity
    partialPosition = Position(PositionConstructorArgs(
      pool=position.pool,
      liquidity=options.liquidityPercentage.multiply(position.liquidity).quotient,
      tickLower=position.tickLower,
      tickUpper=position.tickUpper
    ))
    assert (partialPosition.liquidity > 0), 'ZERO_LIQUIDITY'

    # slippage-adjusted underlying amounts
    amounts = partialPosition.burnAmountsWithSlippage(options.slippageTolerance)
    amount0Min = amounts.amount0
    amount1Min = amounts.amount1

    # remove liquidity
    calldatas.append (
      NonfungiblePositionManager.INTERFACE.encodeFunctionData('decreaseLiquidity', [
        [
          tokenId,
          toHex(partialPosition.liquidity),
          toHex(amount0Min),
          toHex(amount1Min),
          deadline
        ]
      ])
    )

    expectedCurrencyOwed0 = options.collectOptions.expectedCurrencyOwed0
    expectedCurrencyOwed1 = options.collectOptions.expectedCurrencyOwed1

    calldatas += NonfungiblePositionManager.encodeCollect(CollectOptions(
      tokenId=toHex(options.tokenId),
      # add the underlying value to the expected currency already owed
      expectedCurrencyOwed0=expectedCurrencyOwed0.add(CurrencyAmount.fromRawAmount(expectedCurrencyOwed0.currency, amount0Min)),
      expectedCurrencyOwed1=expectedCurrencyOwed1.add(CurrencyAmount.fromRawAmount(expectedCurrencyOwed1.currency, amount1Min)),
      recipient=options.collectOptions.recipient
    ))

    if (options.liquidityPercentage.equalTo(1)):
      if (options.burnToken):
        calldatas.append(NonfungiblePositionManager.INTERFACE.encodeFunctionData('burn', [tokenId]))

    else:
      assert options.burnToken != True, 'CANNOT_BURN'

    return calldatas
  

  @staticmethod
  def safeTransferFromParameters(options: SafeTransferOptions) -> List[CallData]:
    recipient = validateAndParseAddress(options.recipient)
    sender = validateAndParseAddress(options.sender)

    calldata: CallData
    if (options.data):
      calldata = NonfungiblePositionManager.INTERFACE.encodeFunctionData(
        'safeTransferFrom',
        [sender, recipient, toHex(options.tokenId), options.data]
      )
    else:
      calldata = NonfungiblePositionManager.INTERFACE.encodeFunctionData('safeTransferFrom', [
        sender,
        recipient,
        toHex(options.tokenId),
        ''
      ])
    
    return [calldata]
  