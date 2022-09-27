import re

def isEoaAddress(address):
  """
  * Check if input value is a EOA address.
  * @param {any} address - the input value.
  * @return {boolean} returns true if the input value is a EOA address.
  """
  return re.match(r"^(hx)[0-9a-f]{40}$", address) and re.match(r"\S", address)
  
def isScoreAddress(address):
  """
  * Check if input value is a SCORE address. 
  * @param {any} address - the input value. 
  * @return {boolean} returns true if the input value is a SCORE address. 
  """
  return re.match(r"^(cx)[0-9a-f]{40}$", address) and re.match(r"\S", address)
  
def isAddress(address):
  """ 
  * Check if input value is a EOA or SCORE address. 
  * @param {any} address - the input value. 
  * @return {boolean} returns true if the input value is a EOA or SCORE address. 
  """
  return isEoaAddress(address) or isScoreAddress(address)

def validateAndParseAddress (address: str) -> str:
  """
  * Validates an address and returns the parsed version of that address
  * @param address the address
  """
  address = address.strip().lower()

  if isAddress(address):
    return address
  
  raise Exception(f"{address} is not a valid address")

