from typing import Callable, List
import time
from functools import partial

from iconsdk.icon_service import IconService
from iconsdk.wallet.wallet import KeyWallet
from iconsdk.builder.transaction_builder import CallTransactionBuilder
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.builder.call_builder import CallBuilder

from convexus.icontoolkit.calldata import toHex
from convexus.icontoolkit.interface import Interface
from convexus.icontoolkit.asynchronous import make_async

class Sync(object):
  pass

class Contract(object):
  
  def defineAsync(self, name, value):
    self.__dict__[name] = value

  def defineSync(self, name, value):
    self.sync.__dict__[name] = value

  @make_async
  def buildCallArray(self, method: str, output_transform: Callable, *args):
    return self.buildCallArraySync(method, output_transform, *args)

  def buildCallArraySync(self, method: str, output_transform: Callable, *args):
    data = self.interface.encodeFunctionData(method, args)
    result = self.buildCall(method, data)
    if output_transform:
      result = output_transform(result)
    return result

  def buildCall (self, method: str, data: dict):
    txObj = CallBuilder()\
      .to(self.address)\
      .method(method)\
      .params(data['params'] if "params" in data else {})\
      .build()

    return self.iconService.call(txObj)

  @make_async
  def buildSendArray (self, method: str, output_transform: Callable, wallet: KeyWallet, *args):
    return self.buildSendArraySync(method, output_transform, wallet, *args)

  def buildSendArraySync (self, method: str, output_transform: Callable, wallet: KeyWallet, *args):
    if args:
      result = self.buildSendArrayPayable(method, 0, wallet, args)
    else:
      result = self.buildSendArrayPayable(method, 0, wallet)
    
    if output_transform:
      result = output_transform(result)

    return result

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

  @staticmethod
  def getAbi(iconService: IconService, address: str) -> List:
    return iconService.get_score_api(address)

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
    self.sync = Sync()

    for obj in self.interface.abi:
      if obj['type'] == "function":
          name = obj['name']
          output_transform = None
          if 'outputs' in obj and len(obj['outputs']):
            output_type = obj['outputs'][0]['type']
            if output_type == "int":
              output_transform = lambda x: int(x, 0)
            if output_type == "bytes":
              output_transform = lambda x: bytes.fromhex(x.replace("0x", ""))

          # readonly methods
          if 'readonly' in obj and int(obj['readonly'], 16) == 1:
            self.defineAsync(name, partial(self.buildCallArray, name, output_transform))
            self.defineSync(name, partial(self.buildCallArraySync, name, output_transform))
          # write methods
          else:
            self.defineAsync(name, partial(self.buildSendArray, name, output_transform))
            self.defineSync(name, partial(self.buildSendArraySync, name, output_transform))