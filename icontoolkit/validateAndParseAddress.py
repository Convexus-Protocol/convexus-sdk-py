from iconsdk.utils.validation import is_wallet_address, is_score_address

def isAddress (address: str) -> bool:
  return is_wallet_address(address) or is_score_address(address)

def validateAndParseAddress (address: str) -> str:
  """
  * Validates an address and returns the parsed version of that address
  * @param address the address
  """
  address = address.strip().lower()

  if is_wallet_address(address) or is_score_address(address):
    return address
  
  raise Exception("{address} is not a valid address.")

