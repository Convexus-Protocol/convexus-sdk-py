from typing import List
from iconsdk.icon_service import IconService
from functools import partial
from iconsdk.wallet.wallet import KeyWallet
from iconsdk.builder.transaction_builder import CallTransactionBuilder
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.builder.call_builder import CallBuilder
import time
from convexus.icontoolkit.calldata import toHex

from convexus.icontoolkit.interface import Interface

class Contract(object):
  
  def defineReadOnly(self, name, value):
    self.__dict__[name] = value

  def buildCallArray(self, method: str, *args):
    data = self.interface.encodeFunctionData(method, args)
    return self.buildCall(method, data)

  def buildCall (self, method: str, data: dict):
    txObj = CallBuilder()\
      .to(self.address)\
      .method(method)\
      .params(data['params'] if "params" in data else {})\
      .build()

    return self.iconService.call(txObj)

  def buildSendArray (self, method: str, wallet: KeyWallet, *args):
    if args:
      return self.buildSendArrayPayable(method, 0, wallet, args)
    else:
      return self.buildSendArrayPayable(method, 0, wallet)


  def buildSendArrayPayable (self, method: str, icxAmount: int, wallet: KeyWallet, *args):
    data = self.interface.encodeFunctionDataPayable(icxAmount, method, *args)
    return self.buildSend(wallet, data)

  def buildSend (self, wallet: KeyWallet, calldata, waitForResult: bool = False):
    icxValue = calldata["value"] if 'value' in calldata else 0
    return self.buildSendPayable(calldata['to'], calldata['method'], icxValue, wallet, calldata['params'], waitForResult)

  def buildSendPayable (self, to: str, method: str, icxAmount: int, wallet: KeyWallet, params, waitForResult: bool):
    txObjBuilder = CallTransactionBuilder()\
      .method(method)\
      .params(params)\
      .from_(wallet.get_address())\
      .to(to or self.address)\
      .nid(self.nid)\
      .nonce(1)\
      .version(3)\
      .timestamp(int(time.time()) * 1000 * 1000)

    if icxAmount > 0:
      txObjBuilder.value(toHex(icxAmount))
    
    txObjEstimate = txObjBuilder.build()

    # estimate steps
    try:
      steps = self.debugService.estimate_step(txObjEstimate)
    except:
      # Default steps
      steps = 400_000_000

    # add some margin
    steps += 100_000

    txObj = txObjBuilder.step_limit(steps).build()
    signedTx = SignedTransaction(txObj, wallet, steps)
    txhash = self.iconService.send_transaction(signedTx)

    if waitForResult:
      self.iconService.wait_transaction_result(txhash)

    return txhash

  def __init__ (
    self,
    address: str, 
    abi: List, 
    iconService: IconService,
    debugService: IconService,
    nid: int
  ):
    self.iconService = iconService
    self.debugService = debugService
    self.nid = nid
    self.address = address
    self.interface = Interface(abi, address)

    for obj in self.interface.abi:
      if obj['type'] == "function":
          name = obj['name']
          # readonly methods
          if 'readonly' in obj and int(obj['readonly'], 16) == 1:
            buildCallArray = partial(self.buildCallArray, name)
            self.defineReadOnly(name, buildCallArray)
          else:
            buildSendArray = partial(self.buildSendArray, name)
            self.defineReadOnly(name, buildSendArray)