IConvexusStaker = [
    {
        "inputs": [
            {
                "name": "rewardToken",
                "type": "Address"
            },
            {
                "name": "pool",
                "type": "Address"
            },
            {
                "name": "startTime",
                "type": "int"
            },
            {
                "name": "endTime",
                "type": "int"
            },
            {
                "name": "refundee",
                "type": "Address"
            },
            {
                "name": "reward",
                "type": "int"
            }
        ],
        "name": "IncentiveCreated",
        "type": "eventlog"
    },
    {
        "inputs": [
            {
                "name": "incentiveId",
                "type": "bytes"
            },
            {
                "name": "refund",
                "type": "int"
            }
        ],
        "name": "IncentiveEnded",
        "type": "eventlog"
    },
    {
        "inputs": [
            {
                "name": "tokenId",
                "type": "int"
            },
            {
                "name": "oldOwner",
                "type": "Address"
            },
            {
                "name": "newOwner",
                "type": "Address"
            }
        ],
        "name": "DepositTransferred",
        "type": "eventlog"
    },
    {
        "inputs": [
            {
                "name": "tokenId",
                "type": "int"
            },
            {
                "name": "incentiveId",
                "type": "bytes"
            }
        ],
        "name": "TokenUnstaked",
        "type": "eventlog"
    },
    {
        "inputs": [
            {
                "name": "to",
                "type": "Address"
            },
            {
                "name": "reward",
                "type": "int"
            }
        ],
        "name": "RewardClaimed",
        "type": "eventlog"
    },
    {
        "inputs": [
            {
                "name": "tokenId",
                "type": "int"
            },
            {
                "name": "incentiveId",
                "type": "bytes"
            },
            {
                "name": "liquidity",
                "type": "int"
            }
        ],
        "name": "TokenStaked",
        "type": "eventlog"
    },
    {
        "inputs": [
            {
                "fields": [
                    {
                        "name": "rewardToken",
                        "type": "Address"
                    },
                    {
                        "name": "pool",
                        "type": "Address"
                    },
                    {
                        "name": "startTime",
                        "type": "int"
                    },
                    {
                        "name": "endTime",
                        "type": "int"
                    },
                    {
                        "name": "refundee",
                        "type": "Address"
                    }
                ],
                "name": "key",
                "type": "struct"
            }
        ],
        "name": "endIncentive",
        "outputs": [
            {
                "type": "int"
            }
        ],
        "type": "function"
    },
    {
        "inputs": [
            {
                "name": "caller",
                "type": "Address"
            },
            {
                "name": "from",
                "type": "Address"
            },
            {
                "name": "tokenId",
                "type": "int"
            },
            {
                "name": "data",
                "type": "bytes"
            }
        ],
        "name": "onIRC721Received",
        "outputs": [],
        "type": "function"
    },
    {
        "inputs": [
            {
                "name": "tokenId",
                "type": "int"
            },
            {
                "name": "to",
                "type": "Address"
            }
        ],
        "name": "transferDeposit",
        "outputs": [],
        "type": "function"
    },
    {
        "inputs": [
            {
                "name": "tokenId",
                "type": "int"
            },
            {
                "name": "to",
                "type": "Address"
            },
            {
                "name": "data",
                "type": "bytes"
            }
        ],
        "name": "withdrawToken",
        "outputs": [],
        "type": "function"
    },
    {
        "inputs": [
            {
                "fields": [
                    {
                        "name": "rewardToken",
                        "type": "Address"
                    },
                    {
                        "name": "pool",
                        "type": "Address"
                    },
                    {
                        "name": "startTime",
                        "type": "int"
                    },
                    {
                        "name": "endTime",
                        "type": "int"
                    },
                    {
                        "name": "refundee",
                        "type": "Address"
                    }
                ],
                "name": "key",
                "type": "struct"
            },
            {
                "name": "tokenId",
                "type": "int"
            }
        ],
        "name": "stakeToken",
        "outputs": [],
        "type": "function"
    },
    {
        "inputs": [
            {
                "fields": [
                    {
                        "name": "rewardToken",
                        "type": "Address"
                    },
                    {
                        "name": "pool",
                        "type": "Address"
                    },
                    {
                        "name": "startTime",
                        "type": "int"
                    },
                    {
                        "name": "endTime",
                        "type": "int"
                    },
                    {
                        "name": "refundee",
                        "type": "Address"
                    }
                ],
                "name": "key",
                "type": "struct"
            },
            {
                "name": "tokenId",
                "type": "int"
            }
        ],
        "name": "unstakeToken",
        "outputs": [],
        "type": "function"
    },
    {
        "inputs": [
            {
                "name": "rewardToken",
                "type": "Address"
            },
            {
                "name": "to",
                "type": "Address"
            },
            {
                "name": "amountRequested",
                "type": "int"
            }
        ],
        "name": "claimReward",
        "outputs": [
            {
                "type": "int"
            }
        ],
        "type": "function"
    },
    {
        "inputs": [
            {
                "fields": [
                    {
                        "name": "rewardToken",
                        "type": "Address"
                    },
                    {
                        "name": "pool",
                        "type": "Address"
                    },
                    {
                        "name": "startTime",
                        "type": "int"
                    },
                    {
                        "name": "endTime",
                        "type": "int"
                    },
                    {
                        "name": "refundee",
                        "type": "Address"
                    }
                ],
                "name": "key",
                "type": "struct"
            },
            {
                "name": "tokenId",
                "type": "int"
            }
        ],
        "name": "getRewardInfo",
        "outputs": [
            {
                "type": "dict"
            }
        ],
        "readonly": "0x1",
        "type": "function"
    },
    {
        "inputs": [
            {
                "name": "pool",
                "type": "Address"
            },
            {
                "name": "startTime",
                "type": "int"
            },
            {
                "name": "endTime",
                "type": "int"
            },
            {
                "name": "refundee",
                "type": "Address"
            }
        ],
        "name": "createIncentiveIcx",
        "outputs": [],
        "payable": "0x1",
        "type": "function"
    },
    {
        "inputs": [
            {
                "name": "_from",
                "type": "Address"
            },
            {
                "name": "_value",
                "type": "int"
            },
            {
                "default": None,
                "name": "_data",
                "type": "bytes"
            }
        ],
        "name": "tokenFallback",
        "outputs": [],
        "type": "function"
    },
    {
        "inputs": [],
        "name": "name",
        "outputs": [
            {
                "type": "str"
            }
        ],
        "readonly": "0x1",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "factory",
        "outputs": [
            {
                "type": "Address"
            }
        ],
        "readonly": "0x1",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "nonfungiblePositionManager",
        "outputs": [
            {
                "type": "Address"
            }
        ],
        "readonly": "0x1",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "maxIncentiveStartLeadTime",
        "outputs": [
            {
                "type": "int"
            }
        ],
        "readonly": "0x1",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "maxIncentiveDuration",
        "outputs": [
            {
                "type": "int"
            }
        ],
        "readonly": "0x1",
        "type": "function"
    },
    {
        "inputs": [
            {
                "name": "key",
                "type": "bytes"
            }
        ],
        "name": "incentives",
        "outputs": [
            {
                "type": "dict"
            }
        ],
        "readonly": "0x1",
        "type": "function"
    },
    {
        "inputs": [
            {
                "name": "tokenId",
                "type": "int"
            }
        ],
        "name": "deposits",
        "outputs": [
            {
                "type": "dict"
            }
        ],
        "readonly": "0x1",
        "type": "function"
    },
    {
        "inputs": [
            {
                "name": "rewardToken",
                "type": "Address"
            },
            {
                "name": "owner",
                "type": "Address"
            }
        ],
        "name": "rewards",
        "outputs": [
            {
                "type": "int"
            }
        ],
        "readonly": "0x1",
        "type": "function"
    },
    {
        "inputs": [
            {
                "name": "tokenId",
                "type": "int"
            },
            {
                "name": "incentiveId",
                "type": "bytes"
            }
        ],
        "name": "stakes",
        "outputs": [
            {
                "type": "dict"
            }
        ],
        "readonly": "0x1",
        "type": "function"
    }
]