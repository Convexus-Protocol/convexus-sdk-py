IQuoter = [
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
                "name": "path",
                "type": "bytes"
            },
            {
                "name": "sqrtPriceX96",
                "type": "int"
            },
            {
                "name": "tick",
                "type": "int"
            }
        ],
        "name": "convexusSwapCallbackReadonly",
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
                        "name": "tokenIn",
                        "type": "Address"
                    },
                    {
                        "name": "tokenOut",
                        "type": "Address"
                    },
                    {
                        "name": "amountIn",
                        "type": "int"
                    },
                    {
                        "name": "fee",
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
        "name": "quoteExactInputSingle",
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
                        "name": "path",
                        "type": "bytes"
                    },
                    {
                        "name": "amountIn",
                        "type": "int"
                    }
                ],
                "name": "params",
                "type": "struct"
            }
        ],
        "name": "quoteExactInput",
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
                        "name": "tokenIn",
                        "type": "Address"
                    },
                    {
                        "name": "tokenOut",
                        "type": "Address"
                    },
                    {
                        "name": "amount",
                        "type": "int"
                    },
                    {
                        "name": "fee",
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
        "name": "quoteExactOutputSingle",
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
                        "name": "path",
                        "type": "bytes"
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
        "name": "quoteExactOutput",
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
        "name": "readOnlyPool",
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