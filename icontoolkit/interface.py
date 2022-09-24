from typing import List
import json

from icontoolkit.validateAndParseAddress import validateAndParseAddress

class Interface:

  def __init__(self, abi, contractAddress: str) -> None:
    self.abi = abi
    self.contractAddress = contractAddress
    
  def getAbiObject (self, name: str):
    for obj in self.abi:
      if obj['name'] == name:
        return obj
      
    raise Exception(f"INVALID_ABI_NAME: {name}")

  def buildParam (self, value, input):
    inputType = input['type']
    result = {}

    if inputType == "struct":
      assert len(value) == len(input['fields']), "INVALID_STRUCT_COUNT"
      result[input['name']] = {}
      for i in range(len(value)):
        result[input['name']] = result[input['name']] | self.buildParam(value[i], input['fields'][i])

    elif inputType == "Address":
      address = validateAndParseAddress(value)
      result[input['name']] = address

    elif inputType == "int":
      result[input['name']] = hex(value)

    elif inputType == "str":
      result[input['name']] = value

    elif inputType == "bytes":
      result[input['name']] = value
    
    else:
      raise Exception(f"INVALID_PARAM_TYPE: {inputType}")

    return result

  def encodeFunctionDataPayable (self, icxAmount: int, method: str, values: List = None):
    abiObject = self.getAbiObject(method)
    inputs = abiObject['inputs']
    if values is None:
      values = []

    assert len(inputs) == len(values), f"INVALID_ARGS_COUNT (expected {len(inputs)}, got {len(values)})"

    payload: dict = {
      "to": self.contractAddress,
      "method": method,
    }
    
    if icxAmount > 0:
      payload["value"] = hex(icxAmount)

    if len(inputs):
      payload["params"] = {}
      for index in range(len(inputs)):
        payload["params"] = payload["params"] | self.buildParam(values[index], inputs[index])

    return payload

  def encodeFunctionData (self, method, *values):
    return self.encodeFunctionDataPayable(0, method, *values)
  
  def encodeTokenFallbackFunctionData (self, token: str, amount: int, method: str, inputs, values):
    assert len(inputs) == len(values), f"INVALID_ARGS_COUNT (expected ${len(inputs)}, got ${len(values)})"
    
    tokenFallbackPayload = {
      "method": method,
      "params": {}
    }

    if len(inputs) > 0:
      tokenFallbackPayload["params"] = {}
      for index in range(len(inputs)):
        tokenFallbackPayload["params"] = tokenFallbackPayload["params"] | self.buildParam(values[index], inputs[index])
    
    payload = {
      "to": token,
      "method": "transfer",
      "params": {
        "_to": self.contractAddress,
        "_value": hex(amount),
        "_data": "0x" + json.dumps(tokenFallbackPayload).encode().hex()
      }
    }

    return payload