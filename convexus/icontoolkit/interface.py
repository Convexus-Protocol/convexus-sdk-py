from typing import Dict, List
import json
from convexus.icontoolkit.BigInt import BigInt
from convexus.icontoolkit.calldata import toHex
from convexus.icontoolkit.constants import BigintIsh

from convexus.icontoolkit.validateAndParseAddress import validateAndParseAddress

CallData = Dict

class Interface:

  def __init__(self, abi, contractAddress: str) -> None:
    self.abi = abi
    self.contractAddress = contractAddress
    
  def getAbiObject (self, name: str):
    for obj in self.abi:
      if obj['name'] == name:
        return obj
      
    raise Exception(f"INVALID_ABI_NAME: {name}")
  
  def deserialize(self, value, inputType: str):
    if inputType == "Address":
      return validateAndParseAddress(value)
    elif inputType == "int":
      return toHex(value)
    elif inputType == "str":
      return value
    elif inputType == "bytes":
      return value
    elif inputType == "bool":
      return toHex(1 if value else 0)
    else:
      raise Exception(f"INVALID_PARAM_TYPE: {inputType}")

  def buildParam (self, value, input):
    inputType: str = input['type']
    result = {}
    
    # Array
    if inputType.startswith('[]'):
      result[input['name']]: list = []
      for v in value:
        result[input['name']].append(self.deserialize(v, inputType[2:]))

    # Map
    elif inputType == "struct":
      assert len(value) == len(input['fields']), "INVALID_STRUCT_COUNT"
      result[input['name']] = {}
      for i in range(len(value)):
        result[input['name']] = result[input['name']] | self.buildParam(value[i], input['fields'][i])

     # Simple type
    else:
      result[input['name']] = self.deserialize(value, inputType)

    return result

  def encodeFunctionDataPayable (self, icxAmount: BigintIsh, method: str, values: List = None):
    icxAmount = BigInt(icxAmount)
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
      payload["value"] = toHex(icxAmount)

    if len(inputs):
      payload["params"] = {}
      for index in range(len(inputs)):
        payload["params"] = payload["params"] | self.buildParam(values[index], inputs[index])

    return payload

  def encodeFunctionData (self, method, *values):
    return self.encodeFunctionDataPayable(0, method, *values)
  
  def encodeTokenFallbackFunctionData (self, token: str, amount: BigintIsh, method: str, inputs, values):
    amount = BigInt(amount)
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
        "_value": toHex(amount),
        "_data": "0x" + json.dumps(tokenFallbackPayload, separators=(',', ':')).encode().hex()
      }
    }

    return payload