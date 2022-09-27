ISwapRouter = [
    {
        "inputs": [
            {
                "name": "amount0Delta",
                "type": "int"
            },
            {
                "name": "amount1Delta",
                "type": "int"
            },
            {
                "name": "data",
                "type": "bytes"
            }
        ],
        "name": "convexusSwapCallback",
        "outputs": [],
        "type": "function"
    },
    {
        "inputs": [
            {
                "fields": [
                    {
                        "name": "tokenOut",
                        "type": "Address"
                    },
                    {
                        "name": "fee",
                        "type": "int"
                    },
                    {
                        "name": "recipient",
                        "type": "Address"
                    },
                    {
                        "name": "deadline",
                        "type": "int"
                    },
                    {
                        "name": "amountOutMinimum",
                        "type": "int"
                    },
                    {
                        "name": "sqrtPriceLimitX96",
                        "type": "int"
                    }
                ],
                "name": "params",
                "type": "struct"
            }
        ],
        "name": "exactInputSingleIcx",
        "outputs": [],
        "payable": "0x1",
        "type": "function"
    },
    {
        "inputs": [
            {
                "fields": [
                    {
                        "name": "tokenOut",
                        "type": "Address"
                    },
                    {
                        "name": "fee",
                        "type": "int"
                    },
                    {
                        "name": "recipient",
                        "type": "Address"
                    },
                    {
                        "name": "deadline",
                        "type": "int"
                    },
                    {
                        "name": "amountOut",
                        "type": "int"
                    },
                    {
                        "name": "sqrtPriceLimitX96",
                        "type": "int"
                    }
                ],
                "name": "params",
                "type": "struct"
            }
        ],
        "name": "exactOutputSingleIcx",
        "outputs": [],
        "payable": "0x1",
        "type": "function"
    },
    {
        "inputs": [
            {
                "fields": [
                    {
                        "name": "path",
                        "type": "bytes"
                    },
                    {
                        "name": "recipient",
                        "type": "Address"
                    },
                    {
                        "name": "deadline",
                        "type": "int"
                    },
                    {
                        "name": "amountOutMinimum",
                        "type": "int"
                    }
                ],
                "name": "params",
                "type": "struct"
            }
        ],
        "name": "exactInputIcx",
        "outputs": [],
        "payable": "0x1",
        "type": "function"
    },
    {
        "inputs": [
            {
                "fields": [
                    {
                        "name": "path",
                        "type": "bytes"
                    },
                    {
                        "name": "recipient",
                        "type": "Address"
                    },
                    {
                        "name": "deadline",
                        "type": "int"
                    },
                    {
                        "name": "amountOut",
                        "type": "int"
                    }
                ],
                "name": "params",
                "type": "struct"
            }
        ],
        "name": "exactOutputIcx",
        "outputs": [],
        "payable": "0x1",
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
                "name": "token",
                "type": "Address"
            }
        ],
        "name": "withdraw",
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