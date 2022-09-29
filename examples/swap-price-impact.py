from typing import List
from convexus.icontoolkit import Contract
from convexus.sdk import Pool, Tick, Price, TickDataProvider, TickListDataProvider
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
import asyncio, sys

class TicksDB(TickDataProvider):
  def __init__(self, ticks: List[Tick]) -> None:
    super().__init__()
    self.ticks = ticks
    # index => tick mapping
    self.mapped = {tick.index: tick for tick in ticks}

  def getTick(self, tick: int) -> Tick:
    return self.mapped[tick]

  def nextInitializedTickWithinOneWord(self, tick: int, lte: bool, tickSpacing: int):
    return TickListDataProvider(self.ticks, tickSpacing).nextInitializedTickWithinOneWord(tick, lte, tickSpacing)

async def getSortedInitializedTicks(contract) -> List[Tick]:
  # Get amount of initialized ticks
  ticksInitializedSize = await contract.ticksInitializedSize()
  # Get all tick data
  ticksData = await contract.ticksInitializedRange(0, ticksInitializedSize)
  # Convert them to Tick object
  unsortedTicks = map(lambda t: Tick.fromCall(t), ticksData)
  # Sort ticks by index
  ticks = sorted(unsortedTicks, key=lambda x: x.index)
  return ticks

async def main(poolAddress: str):
  # Get Pool instance
  iconService = IconService(HTTPProvider("https://berlin.net.solidwallet.io", 3))
  contract = Contract(poolAddress, Contract.getAbi(iconService, poolAddress), iconService, iconService, 7)
  ticks = await getSortedInitializedTicks(contract)
  pool = await Pool.fromContract(contract)
  pool.tickDataProvider = TicksDB(ticks)

  print(f"Price before = {pool.token0Price.toFixed(2)}")
  result = pool.swap(True, 10**18 * 20)
  print(f"Price after = {Price.fromSqrtPrice(pool.token0, pool.token1, result.sqrtRatioX96).toFixed(2)}")

if len(sys.argv) != 2:
  print(f"Usage: {sys.argv[0]} <pool address>")
  sys.exit(1)

asyncio.run(main(sys.argv[1]))