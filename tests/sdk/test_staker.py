import unittest
from convexus.icontoolkit.expect import expect
from convexus.icontoolkit.BigInt import BigInt

from convexus.sdk.constants import FeeAmount
from convexus.sdkcore.entities.currency import Token
from convexus.sdk.utils.encodeSqrtRatioX96 import encodeSqrtRatioX96
from convexus.sdk.entities.pool import Pool
from convexus.sdk.staker import ClaimOptions, FullWithdrawOptions, IncentiveKey, Staker
from convexus.sdk.nonfungiblePositionManager import NonfungiblePositionManager, SafeTransferOptions
from TestPoolFactoryProvider import TestPoolFactoryProvider

reward = Token('cx1f9840a85d5af5bf1d1762f925bdaddc4201f984', 18, 'r',  'reward')
token0 = Token('cx0000000000000000000000000000000000000001', 18, 't0', 'token0')
token1 = Token('cx0000000000000000000000000000000000000002', 18, 't1', 'token1')

pool_0_1 = Pool(token0, token1, FeeAmount.MEDIUM, encodeSqrtRatioX96(1, 1), 0, 0, [])

incentiveKey = IncentiveKey(
  reward,
  pool_0_1,
  100,
  200,
  'hx0000000000000000000000000000000000000001'
)

incentiveKeys = [incentiveKey]
incentiveKeys.append(IncentiveKey(
  reward,
  pool_0_1,
  50,
  100,
  'hx0000000000000000000000000000000000000089'
))

poolFactoryProvider = TestPoolFactoryProvider()

recipient = 'hx0000000000000000000000000000000000000003'
sender = 'hx0000000000000000000000000000000000000004'
tokenId = 1

class TestStaker(unittest.TestCase):

  def test_succeedsWithAmount(self):
    calldata = Staker.collectRewards(poolFactoryProvider, incentiveKey, ClaimOptions(
      tokenId=tokenId,
      recipient=recipient,
      amount=1
    ))

    expect(calldata).toStrictEqual([
      {
        "to": "ConvexusStaker",
        "method": "unstakeToken",
        "params": {
          "key": {
            "endTime": "0xc8",
            "pool": "cx41ca025441ca025441ca026041ca025441ca027c",
            "refundee": "hx0000000000000000000000000000000000000001",
            "rewardToken": "cx1f9840a85d5af5bf1d1762f925bdaddc4201f984",
            "startTime": "0x64"
          },
          "tokenId": "0x1"
        }
      },
      {
        "to": "ConvexusStaker",
        "method": "claimReward",
        "params": {
          "amountRequested": "0x1",
          "rewardToken": "cx1f9840a85d5af5bf1d1762f925bdaddc4201f984",
          "to": "hx0000000000000000000000000000000000000003"
        }
      },
      {
        "to": "ConvexusStaker",
        "method": "stakeToken",
        "params": {
          "key": {
            "endTime": "0xc8",
            "pool": "cx41ca025441ca025441ca026041ca025441ca027c",
            "refundee": "hx0000000000000000000000000000000000000001",
            "rewardToken": "cx1f9840a85d5af5bf1d1762f925bdaddc4201f984",
            "startTime": "0x64"
          },
          "tokenId": "0x1"
        }
      }
    ])

  def test_succeedsNoAmount(self):
    calldata = Staker.collectRewards(poolFactoryProvider, incentiveKey, ClaimOptions(
      tokenId=tokenId,
      recipient=recipient
    ))

    expect(calldata).toStrictEqual(
      [
        {
            "to": "ConvexusStaker",
            "method": "unstakeToken",
            "params": {
                "key": {
                    "endTime": "0xc8",
                    "pool": "cx41ca025441ca025441ca026041ca025441ca027c",
                    "refundee": "hx0000000000000000000000000000000000000001",
                    "rewardToken": "cx1f9840a85d5af5bf1d1762f925bdaddc4201f984",
                    "startTime": "0x64"
                },
                "tokenId": "0x1"
            }
        },
        {
            "to": "ConvexusStaker",
            "method": "claimReward",
            "params": {
                "amountRequested": "0x0",
                "rewardToken": "cx1f9840a85d5af5bf1d1762f925bdaddc4201f984",
                "to": "hx0000000000000000000000000000000000000003"
            }
        },
        {
            "to": "ConvexusStaker",
            "method": "stakeToken",
            "params": {
                "key": {
                    "endTime": "0xc8",
                    "pool": "cx41ca025441ca025441ca026041ca025441ca027c",
                    "refundee": "hx0000000000000000000000000000000000000001",
                    "rewardToken": "cx1f9840a85d5af5bf1d1762f925bdaddc4201f984",
                    "startTime": "0x64"
                },
                "tokenId": "0x1"
            }
        }
      ]
    )

  def test_succeedsMultipleKeys1(self):
    calldata = Staker.collectRewards(poolFactoryProvider, incentiveKeys, ClaimOptions(
      tokenId=tokenId,
      recipient=recipient
    ))

    expect(calldata).toStrictEqual(
      [
        {
            "to": "ConvexusStaker",
            "method": "unstakeToken",
            "params": {
                "key": {
                    "endTime": "0xc8",
                    "pool": "cx41ca025441ca025441ca026041ca025441ca027c",
                    "refundee": "hx0000000000000000000000000000000000000001",
                    "rewardToken": "cx1f9840a85d5af5bf1d1762f925bdaddc4201f984",
                    "startTime": "0x64"
                },
                "tokenId": "0x1"
            }
        },
        {
            "to": "ConvexusStaker",
            "method": "claimReward",
            "params": {
                "amountRequested": "0x0",
                "rewardToken": "cx1f9840a85d5af5bf1d1762f925bdaddc4201f984",
                "to": "hx0000000000000000000000000000000000000003"
            }
        },
        {
            "to": "ConvexusStaker",
            "method": "stakeToken",
            "params": {
                "key": {
                    "endTime": "0xc8",
                    "pool": "cx41ca025441ca025441ca026041ca025441ca027c",
                    "refundee": "hx0000000000000000000000000000000000000001",
                    "rewardToken": "cx1f9840a85d5af5bf1d1762f925bdaddc4201f984",
                    "startTime": "0x64"
                },
                "tokenId": "0x1"
            }
        },
        {
            "to": "ConvexusStaker",
            "method": "unstakeToken",
            "params": {
                "key": {
                    "endTime": "0x64",
                    "pool": "cx41ca025441ca025441ca026041ca025441ca027c",
                    "refundee": "hx0000000000000000000000000000000000000089",
                    "rewardToken": "cx1f9840a85d5af5bf1d1762f925bdaddc4201f984",
                    "startTime": "0x32"
                },
                "tokenId": "0x1"
            }
        },
        {
            "to": "ConvexusStaker",
            "method": "claimReward",
            "params": {
                "amountRequested": "0x0",
                "rewardToken": "cx1f9840a85d5af5bf1d1762f925bdaddc4201f984",
                "to": "hx0000000000000000000000000000000000000003"
            }
        },
        {
            "to": "ConvexusStaker",
            "method": "stakeToken",
            "params": {
                "key": {
                    "endTime": "0x64",
                    "pool": "cx41ca025441ca025441ca026041ca025441ca027c",
                    "refundee": "hx0000000000000000000000000000000000000089",
                    "rewardToken": "cx1f9840a85d5af5bf1d1762f925bdaddc4201f984",
                    "startTime": "0x32"
                },
                "tokenId": "0x1"
            }
        }
      ]
    )

  def test_succeedsWithOneKeys(self):
    calldata = Staker.withdrawToken(poolFactoryProvider, incentiveKey, FullWithdrawOptions(
      tokenId=tokenId,
      recipient=recipient,
      amount=0,
      owner=sender,
      data='0x0000000000000000000000000000000000000008'
    ))

    expect(calldata).toStrictEqual(
      [
        {
            "to": "ConvexusStaker",
            "method": "unstakeToken",
            "params": {
                "key": {
                    "endTime": "0xc8",
                    "pool": "cx41ca025441ca025441ca026041ca025441ca027c",
                    "refundee": "hx0000000000000000000000000000000000000001",
                    "rewardToken": "cx1f9840a85d5af5bf1d1762f925bdaddc4201f984",
                    "startTime": "0x64"
                },
                "tokenId": "0x1"
            }
        },
        {
            "to": "ConvexusStaker",
            "method": "claimReward",
            "params": {
                "amountRequested": "0x0",
                "rewardToken": "cx1f9840a85d5af5bf1d1762f925bdaddc4201f984",
                "to": "hx0000000000000000000000000000000000000003"
            }
        },
        {
            "to": "ConvexusStaker",
            "method": "withdrawToken",
            "params": {
                "data": "0x0000000000000000000000000000000000000008",
                "to": "hx0000000000000000000000000000000000000004",
                "tokenId": "0x1"
            }
        }
      ]
    )

  def test_succeedsWithMultipleKeys(self):
    calldata = Staker.withdrawToken(poolFactoryProvider, incentiveKeys, FullWithdrawOptions(
      tokenId=tokenId,
      recipient=recipient,
      amount=0,
      owner=sender,
      data='0x0000000000000000000000000000000000000008'
    ))

    expect(calldata).toStrictEqual(
      [
        {
            "to": "ConvexusStaker",
            "method": "unstakeToken",
            "params": {
                "key": {
                    "endTime": "0xc8",
                    "pool": "cx41ca025441ca025441ca026041ca025441ca027c",
                    "refundee": "hx0000000000000000000000000000000000000001",
                    "rewardToken": "cx1f9840a85d5af5bf1d1762f925bdaddc4201f984",
                    "startTime": "0x64"
                },
                "tokenId": "0x1"
            }
        },
        {
            "to": "ConvexusStaker",
            "method": "claimReward",
            "params": {
                "amountRequested": "0x0",
                "rewardToken": "cx1f9840a85d5af5bf1d1762f925bdaddc4201f984",
                "to": "hx0000000000000000000000000000000000000003"
            }
        },
        {
            "to": "ConvexusStaker",
            "method": "unstakeToken",
            "params": {
                "key": {
                    "endTime": "0x64",
                    "pool": "cx41ca025441ca025441ca026041ca025441ca027c",
                    "refundee": "hx0000000000000000000000000000000000000089",
                    "rewardToken": "cx1f9840a85d5af5bf1d1762f925bdaddc4201f984",
                    "startTime": "0x32"
                },
                "tokenId": "0x1"
            }
        },
        {
            "to": "ConvexusStaker",
            "method": "claimReward",
            "params": {
                "amountRequested": "0x0",
                "rewardToken": "cx1f9840a85d5af5bf1d1762f925bdaddc4201f984",
                "to": "hx0000000000000000000000000000000000000003"
            }
        },
        {
            "to": "ConvexusStaker",
            "method": "withdrawToken",
            "params": {
                "data": "0x0000000000000000000000000000000000000008",
                "to": "hx0000000000000000000000000000000000000004",
                "tokenId": "0x1"
            }
        }
      ]
    )

  def test_succeedsSingleKey(self):
    deposit = Staker.encodeDeposit(poolFactoryProvider, incentiveKey)

    expect(deposit).toEqual(
      '0x5b5b22637831663938343061383564356166356266316431373632663932356264616464633432303166393834222c22637834316361303235343431636130323534343163613032363034316361303235343431636130323763222c2230783634222c2230786338222c22687830303030303030303030303030303030303030303030303030303030303030303030303030303031225d5d'
    )

  def test_succeedsMultipleKeys0(self):
    deposit = Staker.encodeDeposit(poolFactoryProvider, incentiveKeys)

    expect(deposit).toEqual(
      '0x5b5b22637831663938343061383564356166356266316431373632663932356264616464633432303166393834222c22637834316361303235343431636130323534343163613032363034316361303235343431636130323763222c2230783634222c2230786338222c22687830303030303030303030303030303030303030303030303030303030303030303030303030303031225d2c5b22637831663938343061383564356166356266316431373632663932356264616464633432303166393834222c22637834316361303235343431636130323534343163613032363034316361303235343431636130323763222c2230783332222c2230783634222c22687830303030303030303030303030303030303030303030303030303030303030303030303030303839225d5d'
    )

  def test_succeeds(self):
    data = Staker.encodeDeposit(poolFactoryProvider, incentiveKey)

    options = SafeTransferOptions(
      sender=sender,
      recipient=recipient,
      tokenId=tokenId,
      data=data
    )
    calldata = NonfungiblePositionManager.safeTransferFromParameters(options)

    expect(calldata).toStrictEqual(
      [
        {
          "to": "NonfungiblePositionManager",
          "method": "safeTransferFrom",
          "params": {
            "from": "hx0000000000000000000000000000000000000004",
            "to": "hx0000000000000000000000000000000000000003",
            "tokenId": "0x1",
            "_data": "0x5b5b22637831663938343061383564356166356266316431373632663932356264616464633432303166393834222c22637834316361303235343431636130323534343163613032363034316361303235343431636130323763222c2230783634222c2230786338222c22687830303030303030303030303030303030303030303030303030303030303030303030303030303031225d5d",
          }
        }
      ]
    )

