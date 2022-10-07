from convexus.sdk import Pool

from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from convexus.icontoolkit import Contract
import asyncio

# Create an ICON service object
httpProvider = HTTPProvider("https://berlin.net.solidwallet.io", 3)
iconService = IconService(httpProvider)

# Create a Pool Contract instance
poolAddress = "cxcc48f601776b5998625017c7d220d09a150aa2ad"
poolAbi = Contract.getAbi(iconService, poolAddress)
poolContract = Contract(poolAddress, poolAbi, iconService, iconService, 7)

async def main ():
  pool = await Pool.fromContract(poolContract)
  print(pool)

asyncio.run(main())