from dataclasses import dataclass
from functools import reduce
from typing import List, Union

from convexus.icontoolkit.pack import pack

from convexus.sdkcore.entities.currency import Token

from convexus.sdk.entities.pool import Pool
from convexus.sdk.entities.route import Route

def encodeRouteToPath (route: Route, exactOutput: bool) -> str:
  """
  * Converts a route to a hex encoded path
  * @param route the pool path to convert to an encoded path
  * @param exactOutput whether the route should be encoded in reverse, for making exact output swaps
  """
  firstInputToken: Token = route.input.wrapped

  @dataclass
  class PackedPath:
    inputToken: Token
    types: List[str]
    path: List[Union[int, str]]

  def reduceEncoding (pp: PackedPath, pool: Pool):
    outputToken = pool.token1 if pool.token0.equals(pp.inputToken) else pool.token0
    if pool == route.pools[0]:
      return PackedPath (
        inputToken=outputToken,
        types=['address', 'uint32', 'address'],
        path=[pp.inputToken.address, pool.fee, outputToken.address]
      )
    else:
      return PackedPath (
        inputToken=outputToken,
        types=pp.types + ['uint32', 'address'],
        path=pp.path + [pool.fee, outputToken.address]
      )

  result = reduce (
    reduceEncoding,
    route.pools,
    PackedPath (
      inputToken=firstInputToken, 
      types=[],
      path=[], 
    )
  )

  path = result.path
  types = result.types

  return pack(list(reversed(types)), list(reversed(path))) if exactOutput else pack(types, path)