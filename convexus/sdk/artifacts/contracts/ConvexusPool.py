IConvexusPool = [
    {
        "inputs": [
            {
                "name": "observationCardinalityNextOld",
                "type": "int"
            },
            {
                "name": "observationCardinalityNextNew",
                "type": "int"
            }
        ],
        "name": "IncreaseObservationCardinalityNext",
        "type": "eventlog"
    },
    {
        "inputs": [
            {
                "name": "sqrtPriceX96",
                "type": "int"
            },
            {
                "name": "tick",
                "type": "int"
            }
        ],
        "name": "Initialized",
        "type": "eventlog"
    },
    {
        "inputs": [
            {
                "indexed": "0x1",
                "name": "recipient",
                "type": "Address"
            },
            {
                "indexed": "0x1",
                "name": "tickLower",
                "type": "int"
            },
            {
                "indexed": "0x1",
                "name": "tickUpper",
                "type": "int"
            },
            {
                "name": "sender",
                "type": "Address"
            },
            {
                "name": "amount",
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
        "name": "Mint",
        "type": "eventlog"
    },
    {
        "inputs": [
            {
                "indexed": "0x1",
                "name": "caller",
                "type": "Address"
            },
            {
                "indexed": "0x1",
                "name": "tickLower",
                "type": "int"
            },
            {
                "indexed": "0x1",
                "name": "tickUpper",
                "type": "int"
            },
            {
                "name": "recipient",
                "type": "Address"
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
        "name": "Collect",
        "type": "eventlog"
    },
    {
        "inputs": [
            {
                "indexed": "0x1",
                "name": "caller",
                "type": "Address"
            },
            {
                "indexed": "0x1",
                "name": "tickLower",
                "type": "int"
            },
            {
                "indexed": "0x1",
                "name": "tickUpper",
                "type": "int"
            },
            {
                "name": "amount",
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
        "name": "Burn",
        "type": "eventlog"
    },
    {
        "inputs": [
            {
                "indexed": "0x1",
                "name": "sender",
                "type": "Address"
            },
            {
                "indexed": "0x1",
                "name": "recipient",
                "type": "Address"
            },
            {
                "name": "amount0",
                "type": "int"
            },
            {
                "name": "amount1",
                "type": "int"
            },
            {
                "name": "sqrtPriceX96",
                "type": "int"
            },
            {
                "name": "liquidity",
                "type": "int"
            },
            {
                "name": "tick",
                "type": "int"
            }
        ],
        "name": "Swap",
        "type": "eventlog"
    },
    {
        "inputs": [
            {
                "indexed": "0x1",
                "name": "sender",
                "type": "Address"
            },
            {
                "indexed": "0x1",
                "name": "recipient",
                "type": "Address"
            },
            {
                "name": "amount0",
                "type": "int"
            },
            {
                "name": "amount1",
                "type": "int"
            },
            {
                "name": "paid0",
                "type": "int"
            },
            {
                "name": "paid1",
                "type": "int"
            }
        ],
        "name": "Flash",
        "type": "eventlog"
    },
    {
        "inputs": [
            {
                "name": "feeProtocol0Old",
                "type": "int"
            },
            {
                "name": "feeProtocol1Old",
                "type": "int"
            },
            {
                "name": "feeProtocol0New",
                "type": "int"
            },
            {
                "name": "feeProtocol1New",
                "type": "int"
            }
        ],
        "name": "SetFeeProtocol",
        "type": "eventlog"
    },
    {
        "inputs": [
            {
                "indexed": "0x1",
                "name": "sender",
                "type": "Address"
            },
            {
                "indexed": "0x1",
                "name": "recipient",
                "type": "Address"
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
        "name": "CollectProtocol",
        "type": "eventlog"
    },
    {
        "inputs": [
            {
                "name": "observationCardinalityNext",
                "type": "int"
            }
        ],
        "name": "increaseObservationCardinalityNext",
        "outputs": [],
        "type": "function"
    },
    {
        "inputs": [
            {
                "name": "sqrtPriceX96",
                "type": "int"
            }
        ],
        "name": "initialize",
        "outputs": [],
        "type": "function"
    },
    {
        "inputs": [
            {
                "name": "recipient",
                "type": "Address"
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
                "name": "amount",
                "type": "int"
            },
            {
                "name": "data",
                "type": "bytes"
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
                "name": "recipient",
                "type": "Address"
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
                "name": "amount0Requested",
                "type": "int"
            },
            {
                "name": "amount1Requested",
                "type": "int"
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
                "name": "tickLower",
                "type": "int"
            },
            {
                "name": "tickUpper",
                "type": "int"
            },
            {
                "name": "amount",
                "type": "int"
            }
        ],
        "name": "burn",
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
                "name": "recipient",
                "type": "Address"
            },
            {
                "name": "zeroForOne",
                "type": "bool"
            },
            {
                "name": "amountSpecified",
                "type": "int"
            },
            {
                "name": "sqrtPriceLimitX96",
                "type": "int"
            },
            {
                "name": "data",
                "type": "bytes"
            }
        ],
        "name": "swap",
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
                "name": "recipient",
                "type": "Address"
            },
            {
                "name": "amount0",
                "type": "int"
            },
            {
                "name": "amount1",
                "type": "int"
            },
            {
                "name": "data",
                "type": "bytes"
            }
        ],
        "name": "flash",
        "outputs": [],
        "type": "function"
    },
    {
        "inputs": [
            {
                "name": "feeProtocol0",
                "type": "int"
            },
            {
                "name": "feeProtocol1",
                "type": "int"
            }
        ],
        "name": "setFeeProtocol",
        "outputs": [],
        "type": "function"
    },
    {
        "inputs": [
            {
                "name": "recipient",
                "type": "Address"
            },
            {
                "name": "amount0Requested",
                "type": "int"
            },
            {
                "name": "amount1Requested",
                "type": "int"
            }
        ],
        "name": "collectProtocol",
        "outputs": [
            {
                "type": "dict"
            }
        ],
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
                "name": "tickLower",
                "type": "int"
            },
            {
                "name": "tickUpper",
                "type": "int"
            }
        ],
        "name": "snapshotCumulativesInside",
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
                "name": "secondsAgos",
                "type": "[]int"
            }
        ],
        "name": "observe",
        "outputs": [
            {
                "type": "dict"
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
    },
    {
        "inputs": [],
        "name": "token0",
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
        "name": "token1",
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
        "name": "settings",
        "outputs": [
            {
                "type": "dict"
            }
        ],
        "readonly": "0x1",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "slot0",
        "outputs": [
            {
                "type": "dict"
            }
        ],
        "readonly": "0x1",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "protocolFees",
        "outputs": [
            {
                "type": "dict"
            }
        ],
        "readonly": "0x1",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "maxLiquidityPerTick",
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
        "name": "liquidity",
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
        "name": "fee",
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
        "name": "tickSpacing",
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
        "name": "feeGrowthGlobal0X128",
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
        "name": "feeGrowthGlobal1X128",
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
                "name": "tick",
                "type": "int"
            }
        ],
        "name": "ticks",
        "outputs": [
            {
                "type": "dict"
            }
        ],
        "readonly": "0x1",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "ticksInitializedSize",
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
        "name": "ticksInitialized",
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
                "name": "index",
                "type": "int"
            }
        ],
        "name": "observations",
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
                "name": "index",
                "type": "int"
            }
        ],
        "name": "tickBitmap",
        "outputs": [
            {
                "type": "int"
            }
        ],
        "readonly": "0x1",
        "type": "function"
    }
]