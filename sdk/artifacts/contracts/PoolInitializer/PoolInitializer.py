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