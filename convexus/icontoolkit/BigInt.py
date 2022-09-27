from convexus.icontoolkit.constants import BigintIsh

def BigInt(i: BigintIsh) -> int:
  if not isinstance(i, BigintIsh):
    raise Exception(f"Invalid BigintIsh type: {type(i)}")

  if isinstance(i, str):
    return int(i, 0)
  return i