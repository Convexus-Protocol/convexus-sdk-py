IIRC2 = [
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
      "inputs": [],
      "name": "decimals",
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
              "name": "_owner",
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
              "name": "_to",
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
      "name": "transfer",
      "outputs": [],
      "type": "function"
  },
  {
      "inputs": [
          {
              "indexed": "0x1",
              "name": "_from",
              "type": "Address"
          },
          {
              "indexed": "0x1",
              "name": "_to",
              "type": "Address"
          },
          {
              "indexed": "0x1",
              "name": "_value",
              "type": "int"
          },
          {
              "name": "_data",
              "type": "bytes"
          }
      ],
      "name": "Transfer",
      "type": "eventlog"
  }
]