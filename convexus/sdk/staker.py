from dataclasses import dataclass
import json
from abc import ABCMeta
from typing import List, Tuple
from convexus.icontoolkit.calldata import toHex

from convexus.icontoolkit.constants import BigintIsh
from convexus.icontoolkit.interface import CallData, Interface
from convexus.icontoolkit.validateAndParseAddress import validateAndParseAddress
from convexus.sdkcore.entities.currency import Token

from convexus.sdk.entities.factoryProvider import PoolFactoryProvider
from convexus.sdk.entities.pool import Pool

from convexus.sdk.artifacts.contracts.ConvexusStaker import IConvexusStaker

from collections.abc import Sequence

# ClaimOptions & WithdrawOptions

@dataclass
class FullWithdrawOptions:
  """
   * The id of the NFT
  """
  tokenId: BigintIsh

  """
   * Address to send rewards to.
  """
  recipient: str

  """
   * Set when withdrawing. The position will be sent to `owner` on withdraw.
  """
  owner: str

  """
   * The amount of `rewardToken` to claim. 0 claims all.
  """
  amount: BigintIsh | None = None

  """
   * Set when withdrawing. `data` is passed to `safeTransferFrom` when transferring the position from contract back to owner.
  """
  data: str | None = None


@dataclass
class IncentiveKey:
  """
  * Represents a unique staking program.
  """

  """
   * The token rewarded for participating in the staking program.
  """
  rewardToken: Token
  """
   * The pool that the staked positions must provide in.
  """
  pool: Pool
  """
   * The time when the incentive program begins.
  """
  startTime: BigintIsh
  """
   * The time that the incentive program ends.
  """
  endTime: BigintIsh
  """
   * The address which receives any remaining reward tokens at `endTime`.
  """
  refundee: str

@dataclass
class ClaimOptions:
  """
  * Options to specify when claiming rewards.
  """

  """
   * The id of the NFT
  """
  tokenId: BigintIsh

  """
   * Address to send rewards to.
  """
  recipient: str

  """
   * The amount of `rewardToken` to claim. 0 claims all.
  """
  amount: BigintIsh | None = None

@dataclass
class WithdrawOptions:
  """
  * Options to specify when withdrawing a position.
  """

  """
   * Set when withdrawing. The position will be sent to `owner` on withdraw.
  """
  owner: str

  """
   * Set when withdrawing. `data` is passed to `safeTransferFrom` when transferring the position from contract back to owner.
  """
  data: str | None

class Staker(metaclass=ABCMeta):
  INTERFACE: Interface = Interface(IConvexusStaker, "ConvexusStaker")

  @staticmethod
  def setContractAddress (contractAddress: str):
    Staker.INTERFACE = Interface(IConvexusStaker, contractAddress)

  @staticmethod
  def encodeClaim (
    poolFactoryProvider: PoolFactoryProvider, 
    incentiveKey: IncentiveKey, 
    options: ClaimOptions
  ) -> List[CallData]:
    """
    *  To claim rewards, must unstake and then claim.
    * @param incentiveKey The unique identifier of a staking program.
    * @param options Options for producing the calldata to claim. Can't claim unless you unstake.
    * @returns The calldatas for 'unstakeToken' and 'claimReward'.
    """

    calldatas: List[CallData] = []
    calldatas.append (
      Staker.INTERFACE.encodeFunctionData('unstakeToken', [
        Staker._encodeIncentiveKey(poolFactoryProvider, incentiveKey),
        toHex(options.tokenId)
      ])
    )

    recipient: str = validateAndParseAddress(options.recipient)
    amount = options.amount if options.amount else 0
    calldatas.append (
      Staker.INTERFACE.encodeFunctionData('claimReward', [incentiveKey.rewardToken.address, recipient, toHex(amount)])
    )
    return calldatas

  @staticmethod
  def collectRewards(
    poolFactoryProvider: PoolFactoryProvider, 
    incentiveKeys: IncentiveKey | List[IncentiveKey], 
    options: ClaimOptions
  ) -> List[CallData]:
    """
    * Note:  A `tokenId` can be staked in many programs but to claim rewards and continue the program you must unstake, claim, and then restake.
    * @param incentiveKeys An IncentiveKey or array of IncentiveKeys that `tokenId` is staked in.
    * Input an array of IncentiveKeys to claim rewards for each program.
    * @param options ClaimOptions to specify tokenId, recipient, and amount wanting to collect.
    * Note that you can only specify one amount and one recipient across the various programs if you are collecting from multiple programs at once.
    * @returns
    """
    incentiveKeys = incentiveKeys if isinstance(incentiveKeys, Sequence) else [incentiveKeys]
    calldatas: List[CallData] = []

    for i in range(len(incentiveKeys)):
      # the unique program tokenId is staked in
      incentiveKey = incentiveKeys[i]
      # unstakes and claims for the unique program
      calldatas += Staker.encodeClaim(poolFactoryProvider, incentiveKey, options)
      # re-stakes the position for the unique program
      calldatas.append (
        Staker.INTERFACE.encodeFunctionData('stakeToken', [
          Staker._encodeIncentiveKey(poolFactoryProvider, incentiveKey),
          toHex(options.tokenId)
        ])
      )

    return calldatas

  @staticmethod
  def withdrawToken (
    poolFactoryProvider: PoolFactoryProvider,
    incentiveKeys: IncentiveKey | List[IncentiveKey],
    withdrawOptions: FullWithdrawOptions
  ) -> List[CallData]:
    """
    * @param incentiveKeys A list of incentiveKeys to unstake from. Should include all incentiveKeys (unique staking programs) that `options.tokenId` is staked in.
    * @param withdrawOptions Options for producing claim calldata and withdraw calldata. Can't withdraw without unstaking all programs for `tokenId`.
    * @returns Calldata for unstaking, claiming, and withdrawing.
    """
    calldatas: List[CallData] = []

    incentiveKeys = incentiveKeys if isinstance(incentiveKeys, Sequence) else [incentiveKeys]

    claimOptions = ClaimOptions(
      tokenId=withdrawOptions.tokenId,
      recipient=withdrawOptions.recipient,
      amount=withdrawOptions.amount
    )

    for i in range(len(incentiveKeys)):
      incentiveKey = incentiveKeys[i]
      calldatas += Staker.encodeClaim(poolFactoryProvider, incentiveKey, claimOptions)

    owner = validateAndParseAddress(withdrawOptions.owner)
    calldatas.append (
      Staker.INTERFACE.encodeFunctionData('withdrawToken', [
        toHex(withdrawOptions.tokenId),
        owner,
        withdrawOptions.data if withdrawOptions.data else toHex(0)
      ])
    )
    return calldatas

  @staticmethod
  def encodeDeposit (
    poolFactoryProvider: PoolFactoryProvider, 
    incentiveKeys: IncentiveKey | List[IncentiveKey]
  ) -> str:
    """
    * @param incentiveKeys A single IncentiveKey or array of IncentiveKeys to be encoded and used in the data parameter in `safeTransferFrom`
    * @returns An IncentiveKey as a string
    """
    incentiveKeys = incentiveKeys if isinstance(incentiveKeys, Sequence) else [incentiveKeys]
    data: List[Tuple[str, str, str, str, str]]

    if (len(incentiveKeys) > 1):
      keys = []
      for i in range(len(incentiveKeys)):
        incentiveKey = incentiveKeys[i]
        keys.append (Staker._encodeIncentiveKey(poolFactoryProvider, incentiveKey))

      data = keys
    else:
      data = [Staker._encodeIncentiveKey(poolFactoryProvider, incentiveKeys[0])]

    # FIXME: RLP encode instead of JSON encode
    return "0x" + json.dumps(data, separators=(',', ':')).encode('utf-8').hex()

  @staticmethod
  def _encodeIncentiveKey(
    poolFactoryProvider: PoolFactoryProvider,
    incentiveKey: IncentiveKey
  ) -> Tuple[str, str, str, str, str]:
    """
    * @param incentiveKey An `IncentiveKey` which represents a unique staking program.
    * @returns An encoded IncentiveKey to be read
    """
    pool = incentiveKey.pool
    refundee = validateAndParseAddress(incentiveKey.refundee)
    return (
      incentiveKey.rewardToken.address,
      Pool.getAddress(poolFactoryProvider, pool.token0, pool.token1, pool.fee),
      toHex(incentiveKey.startTime),
      toHex(incentiveKey.endTime),
      refundee
    )
