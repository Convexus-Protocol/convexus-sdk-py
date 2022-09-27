from convexus.icontoolkit.validateAndParseAddress import isAddress
from iconsdk.utils.validation import is_wallet_address
import struct

def uint32ToBytes(num: int):
  return int.to_bytes(num, 4, "big")

def addressToBytes (address: str):
  if not isAddress(address):
    raise Exception(f"Invalid address {address}")

  isEoa = is_wallet_address(address)
  hexAddress = bytes.fromhex(address[2:])
  prefix = b"\x00" if isEoa else b"\x01"

  return prefix + hexAddress

def packSingle (type: str, value):
  if type == "address":
    return addressToBytes(value)
  elif type == "string":
    return value.encode('utf-8')
  elif type == "bytes":
    return value
  elif type == "uint32":
    return uint32ToBytes(value)
  else:
    raise Exception(f"invalid type : {type}")

def concat (arrays):
  result = bytearray()
  for array in arrays:
    result += array
  return result

def pack (types, values):
  if not types:
    types = []
  if not values:
    values = []
  
  if len(types) != len(values):
    raise Exception(f"Wrong number of values; expected {len(types)}, got {len(values)}")

  tight = []

  for index, type in enumerate(types):
    tight.append(packSingle(type, values[index]))

  return "0x" + concat(tight).hex()
