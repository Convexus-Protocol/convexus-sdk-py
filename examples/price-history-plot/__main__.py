from convexus.sdk import Pool, OracleObservation
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from convexus.icontoolkit import Contract
from convexus.sdk.utils.priceTickConversions import tickToPrice

import seaborn as sns, time, sys, asyncio
import matplotlib.pyplot as plt
import requests, time, json
from datetime import datetime, timezone

from convexus.sdkcore.entities.fractions.price import Price

def get_utc_timestamp() -> int:
  dt = datetime.now(timezone.utc)
  utc_time = dt.replace(tzinfo=timezone.utc)
  return utc_time.timestamp()

async def main (poolAddress: str):
  # Create an ICON service object
  httpProvider = HTTPProvider("https://berlin.net.solidwallet.io", 3)
  iconService = IconService(httpProvider)

  # Create a Pool Contract instance
  poolAbi = Contract.getAbi(iconService, poolAddress)
  poolContract = Contract(poolAddress, poolAbi, iconService, iconService, 7)
  pool = await Pool.fromContract(poolContract)
  
  # Get history items
  r = requests.get(
    'http://127.0.0.1:8000/intrinsics/get', 
    params={
      'pool_address': poolAddress,
      'timestamp': int(get_utc_timestamp() - 3600) # last day
    }
  )
  intrinsics = json.loads(r.text)

  data = {}
  for info in intrinsics:
    data[datetime.fromtimestamp(info['timestamp'])] = float(Price.fromSqrtPrice(pool.token0, pool.token1, info['sqrtPriceX96']).toFixed(5))

  # Plot chronogically
  x = list(data.keys())
  y = list(reversed(data.values()))
  sns.set_theme()
  plt.plot(x, y)
  plt.title(f"{pool.token0.symbol} / {pool.token1.symbol} Price")
  plt.xlabel("Time")
  plt.ylabel("Price")
  plt.show()

if len(sys.argv) != 2:
  print(f"Usage: {sys.argv[0]} <pool address>")
  sys.exit(1)

asyncio.run(main(sys.argv[1]))