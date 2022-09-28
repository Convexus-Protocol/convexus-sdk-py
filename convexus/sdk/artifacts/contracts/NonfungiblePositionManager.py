INonfungiblePositionManager = [
    {
        "inputs": [
            {
                "name": "from",
                "type": "Address"
            },
            {
                "name": "to",
                "type": "Address"
            },
            {
                "name": "tokenId",
                "type": "int"
            }
        ],
        "name": "Transfer",
        "type": "eventlog"
    },
    {
        "inputs": [
            {
                "name": "ownerOf",
                "type": "Address"
            },
            {
                "name": "to",
                "type": "Address"
            },
            {
                "name": "tokenId",
                "type": "int"
            }
        ],
        "name": "Approval",
        "type": "eventlog"
    },
    {
        "inputs": [
            {
                "name": "owner",
                "type": "Address"
            },
            {
                "name": "operator",
                "type": "Address"
            },
            {
                "name": "approved",
                "type": "bool"
            }
        ],
        "name": "ApprovalForAll",
        "type": "eventlog"
    },
    {
        "inputs": [
            {
                "name": "owner",
                "type": "Address"
            }
        ],
        "name": "balanceOf",
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
            }
        ],
        "name": "ownerOf",
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
        "name": "symbol",
        "outputs": [
            {
                "type": "str"
            }
        ],
        "readonly": "0x1",
        "type": "function"
    },
    {
        "inputs": [
            {
                "name": "to",
                "type": "Address"
            },
            {
                "name": "tokenId",
                "type": "int"
            }
        ],
        "name": "approve",
        "outputs": [],
        "type": "function"
    },
    {
        "inputs": [
            {
                "name": "operator",
                "type": "Address"
            },
            {
                "name": "approved",
                "type": "bool"
            }
        ],
        "name": "setApprovalForAll",
        "outputs": [],
        "type": "function"
    },
    {
        "inputs": [
            {
                "name": "owner",
                "type": "Address"
            },
            {
                "name": "operator",
                "type": "Address"
            }
        ],
        "name": "isApprovedForAll",
        "outputs": [
            {
                "type": "bool"
            }
        ],
        "readonly": "0x1",
        "type": "function"
    },
    {
        "inputs": [
            {
                "name": "from",
                "type": "Address"
            },
            {
                "name": "to",
                "type": "Address"
            },
            {
                "name": "tokenId",
                "type": "int"
            }
        ],
        "name": "transferFrom",
        "outputs": [],
        "type": "function"
    },
    {
        "inputs": [
            {
                "name": "from",
                "type": "Address"
            },
            {
                "name": "to",
                "type": "Address"
            },
            {
                "name": "tokenId",
                "type": "int"
            },
            {
                "default": None,
                "name": "_data",
                "type": "bytes"
            }
        ],
        "name": "safeTransferFrom",
        "outputs": [],
        "type": "function"
    },
    {
        "inputs": [
            {
                "name": "owner",
                "type": "Address"
            },
            {
                "name": "index",
                "type": "int"
            }
        ],
        "name": "tokenOfOwnerByIndex",
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
        "name": "totalSupply",
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
                "name": "index",
                "type": "int"
            }
        ],
        "name": "tokenByIndex",
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
                "name": "liquidity",
                "type": "int"
            },
            {
                "name": "amount0",
                "type": "int"
            },
            {
                "name": "amount1",
                "type": "int"
            }
        ],
        "name": "IncreaseLiquidity",
        "type": "eventlog"
    },
    {
        "inputs": [
            {
                "name": "tokenId",
                "type": "int"
            },
            {
                "name": "liquidity",
                "type": "int"
            },
            {
                "name": "amount0",
                "type": "int"
            },
            {
                "name": "amount1",
                "type": "int"
            }
        ],
        "name": "DecreaseLiquidity",
        "type": "eventlog"
    },
    {
        "inputs": [
            {
                "name": "tokenId",
                "type": "int"
            },
            {
                "name": "recipient",
                "type": "Address"
            },
            {
                "name": "amount0Collect",
                "type": "int"
            },
            {
                "name": "amount1Collect",
                "type": "int"
            }
        ],
        "name": "Collect",
        "type": "eventlog"
    },
    {
        "inputs": [
            {
                "name": "tokenId",
                "type": "int"
            }
        ],
        "name": "positions",
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
                "fields": [
                    {
                        "name": "token0",
                        "type": "Address"
                    },
                    {
                        "name": "token1",
                        "type": "Address"
                    },
                    {
                        "name": "fee",
                        "type": "int"
                    },
                    {
                        "name": "tickLower",
                        "type": "int"
                    },
                    {
                        "name": "tickUpper",
                        "type": "int"
                    },
                    {
                        "name": "amount0Desired",
                        "type": "int"
                    },
                    {
                        "name": "amount1Desired",
                        "type": "int"
                    },
                    {
                        "name": "amount0Min",
                        "type": "int"
                    },
                    {
                        "name": "amount1Min",
                        "type": "int"
                    },
                    {
                        "name": "recipient",
                        "type": "Address"
                    },
                    {
                        "name": "deadline",
                        "type": "int"
                    }
                ],
                "name": "params",
                "type": "struct"
            }
        ],
        "name": "mint",
        "outputs": [
            {
                "type": "dict"
            }
        ],
        "type": "function"
    },
    {
        "inputs": [
            {
                "name": "tokenId",
                "type": "int"
            }
        ],
        "name": "tokenURI",
        "outputs": [
            {
                "type": "str"
            }
        ],
        "readonly": "0x1",
        "type": "function"
    },
    {
        "inputs": [
            {
                "fields": [
                    {
                        "name": "tokenId",
                        "type": "int"
                    },
                    {
                        "name": "amount0Desired",
                        "type": "int"
                    },
                    {
                        "name": "amount1Desired",
                        "type": "int"
                    },
                    {
                        "name": "amount0Min",
                        "type": "int"
                    },
                    {
                        "name": "amount1Min",
                        "type": "int"
                    },
                    {
                        "name": "deadline",
                        "type": "int"
                    }
                ],
                "name": "params",
                "type": "struct"
            }
        ],
        "name": "increaseLiquidity",
        "outputs": [
            {
                "type": "dict"
            }
        ],
        "type": "function"
    },
    {
        "inputs": [
            {
                "fields": [
                    {
                        "name": "tokenId",
                        "type": "int"
                    },
                    {
                        "name": "liquidity",
                        "type": "int"
                    },
                    {
                        "name": "amount0Min",
                        "type": "int"
                    },
                    {
                        "name": "amount1Min",
                        "type": "int"
                    },
                    {
                        "name": "deadline",
                        "type": "int"
                    }
                ],
                "name": "params",
                "type": "struct"
            }
        ],
        "name": "decreaseLiquidity",
        "outputs": [
            {
                "type": "dict"
            }
        ],
        "type": "function"
    },
    {
        "inputs": [
            {
                "fields": [
                    {
                        "name": "tokenId",
                        "type": "int"
                    },
                    {
                        "name": "recipient",
                        "type": "Address"
                    },
                    {
                        "name": "amount0Max",
                        "type": "int"
                    },
                    {
                        "name": "amount1Max",
                        "type": "int"
                    }
                ],
                "name": "params",
                "type": "struct"
            }
        ],
        "name": "collect",
        "outputs": [
            {
                "type": "dict"
            }
        ],
        "type": "function"
    },
    {
        "inputs": [
            {
                "name": "tokenId",
                "type": "int"
            }
        ],
        "name": "burn",
        "outputs": [],
        "type": "function"
    },
    {
        "inputs": [
            {
                "name": "amount0Owed",
                "type": "int"
            },
            {
                "name": "amount1Owed",
                "type": "int"
            },
            {
                "name": "data",
                "type": "bytes"
            }
        ],
        "name": "convexusMintCallback",
        "outputs": [],
        "type": "function"
    },
    {
        "inputs": [
            {
                "name": "token",
                "type": "Address"
            }
        ],
        "name": "withdraw",
        "outputs": [],
        "type": "function"
    },
    {
        "inputs": [],
        "name": "depositIcx",
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
        "inputs": [
            {
                "name": "user",
                "type": "Address"
            },
            {
                "name": "token",
                "type": "Address"
            }
        ],
        "name": "deposited",
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
                "name": "user",
                "type": "Address"
            }
        ],
        "name": "depositedTokensSize",
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
                "name": "user",
                "type": "Address"
            },
            {
                "name": "index",
                "type": "int"
            }
        ],
        "name": "depositedToken",
        "outputs": [
            {
                "type": "Address"
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
        "name": "getApproved",
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
    }
]