from convexus.sdk import Pool, OracleObservation
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from convexus.icontoolkit import Contract
from convexus.sdk.utils.priceTickConversions import tickToPrice

import seaborn as sns, time, sys, asyncio
import matplotlib.pyplot as plt

async def main (poolAddress: str):
  # Create an ICON service object
  httpProvider = HTTPProvider("https://berlin.net.solidwallet.io", 3)
  iconService = IconService(httpProvider)

  # Create a Pool Contract instance
  poolAbi = Contract.getAbi(iconService, poolAddress)
  poolContract = Contract(poolAddress, poolAbi, iconService, iconService, 7)
  pool = await Pool.fromContract(poolContract)
  
  # Get oldest oracle entry
  oldestObservation = OracleObservation.fromCall(await poolContract.oldestObservation())
  oldestTime = int(time.time() - oldestObservation.blockTimestamp) - 1

  # Get about ~250 TWAPs
  secondsAgo = list(range(0, oldestTime, oldestTime // 250))
  result = await poolContract.observe(secondsAgo)
  tickCumulatives = list(map(lambda x: int(x, 0), result['tickCumulatives']))

  data = {}
  for i in range(1, len(tickCumulatives)):
    tickCumulativesDelta = tickCumulatives[0] - tickCumulatives[i]
    arithmeticMeanTick = tickCumulativesDelta // secondsAgo[i]
    data[secondsAgo[i]] = arithmeticMeanTick

  # Map seconds => minutes: tick => price
  data = {k/60: float(tickToPrice(pool.token0, pool.token1, v).toFixed(5)) for k, v in data.items()}

  # Plot chronogically
  x = list(data.keys())
  y = list(reversed(data.values()))
  sns.set_theme()
  plt.plot(x, y)
  plt.title(f"{pool.token0.symbol} / {pool.token1.symbol} Price")
  plt.xlabel("Time (minutes)")
  plt.ylabel("Price")
  plt.show()

if len(sys.argv) != 2:
  print(f"Usage: {sys.argv[0]} <pool address>")
  sys.exit(1)

asyncio.run(main(sys.argv[1]))