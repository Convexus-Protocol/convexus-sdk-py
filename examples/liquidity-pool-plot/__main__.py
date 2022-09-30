from typing import List
from convexus.icontoolkit import Contract
from convexus.sdk import Pool, Tick
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
import asyncio, sys
import matplotlib.pyplot as plt
import seaborn as sns

from convexus.sdk.utils.priceTickConversions import tickToPrice

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
  pool = await Pool.fromContract(contract)
  ticks = await getSortedInitializedTicks(contract)
  # index => liquidity mapping
  tickLiquidityMapping = {tick.index: tick.liquidityNet for tick in ticks}
  
  # Get min/max ticks
  minTick = ticks[0].index
  maxTick = ticks[-1].index

  # Build data to plot
  # Start with 0 liquidity on the left of the chart
  data = {}
  liquidity = 0
  for tick in range(minTick, maxTick + 1, pool.tickSpacing):
    liquidityDelta = tickLiquidityMapping.get(tick, 0)
    if liquidityDelta != 0:
      data[tick-pool.tickSpacing] = liquidity // 10**18
      liquidity += liquidityDelta
      data[tick] = liquidity // 10**18

  # remap tick key to price
  data = {int(tickToPrice(pool.token0, pool.token1, k).toFixed(0)): int(v) for k, v in data.items()}

  # Plot
  x = list(data.keys())
  y = list(data.values())
  sns.set_theme()
  plt.plot(x, y)
  plt.fill(x, y, alpha=0.5)
  plt.xlabel("Price")
  plt.ylabel("Liquidity")
  plt.axvline(x = int(pool.token0Price.toFixed(0)), color='r')
  plt.show()

if len(sys.argv) != 2:
  print(f"Usage: {sys.argv[0]} <pool address>")
  sys.exit(1)

asyncio.run(main(sys.argv[1]))