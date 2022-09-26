from typing import NamedTuple
from sdkcore.entities.fractions.percent import Percent

class FeeOptions(NamedTuple):
  """
   * The percent of the output that will be taken as a fee.
  """
  fee: Percent

  """
   * The recipient of the fee.
  """
  recipient: str
