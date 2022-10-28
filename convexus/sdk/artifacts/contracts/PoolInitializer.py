IPoolInitializer = [
    {
        "inputs": [
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
                "name": "sqrtPriceX96",
                "type": "int"
            }
        ],
        "name": "createAndInitializePoolIfNecessary",
        "outputs": [
            {
                "type": "Address"
            }
        ],
        "type": "function"
    },
    {
        "inputs": [
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
                "name": "sqrtPriceX96",
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
                "name": "amount0",
                "type": "int"
            },
            {
                "name": "amount1",
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
        "name": "createAndInitializePoolIfNecessaryAndMintPosition",
        "outputs": [
            {
                "type": "dict"
            }
        ],
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
    }
]