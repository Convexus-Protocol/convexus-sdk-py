from dataclasses import dataclass
from convexus.sdkcore.entities.fractions.percent import Percent

@dataclass
class FeeOptions:
  """
   * The percent of the output that will be taken as a fee.
  """
  fee: Percent

  """
   * The recipient of the fee.
  """
  recipient: str
