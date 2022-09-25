from icontoolkit.constants import BigintIsh

def BigInt(i: BigintIsh) -> int:
  if isinstance(i, str):
    return int(i, 0)
  return i