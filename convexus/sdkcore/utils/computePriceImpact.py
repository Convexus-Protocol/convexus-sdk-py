from convexus.sdkcore.entities.fractions.currencyAmount import CurrencyAmount
from convexus.sdkcore.entities.fractions.percent import Percent
from convexus.sdkcore.entities.fractions.price import Price

def computePriceImpact (
  midPrice: Price,
  inputAmount: CurrencyAmount,
  outputAmount: CurrencyAmount
) -> Percent:
  """
  * Returns the percent difference between the mid price and the execution price, i.e. price impact.
  * @param midPrice mid price before the trade
  * @param inputAmount the input amount of the trade
  * @param outputAmount the output amount of the trade
  """
  quotedOutputAmount = midPrice.quote(inputAmount)
  # calculate price impact := (exactQuote - outputAmount) / exactQuote
  priceImpact = quotedOutputAmount.subtract(outputAmount).divide(quotedOutputAmount)
  return Percent(priceImpact.numerator, priceImpact.denominator)
