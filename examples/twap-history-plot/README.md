## Plot Convexus TWAP Oracle

Convexus Price Oracle provides a reliable weighted-price history of any given Convexus Pool.
Please read more about this concept here : https://docs.uniswap.org/protocol/V2/concepts/core-concepts/oracles

### Install
```bash
$ python -m venv venv
$ source ./venv/bin/activate
$ pip install -r ./examples/price-history-plot/requirements.txt
```

### Usage

```bash
$ python ./examples/price-history-plot <pool address>
```

### Example

```bash
$ python ./examples/price-history-plot cxddee489ae0d33e98b73dc30144afdd892fe43816
```


![preview](https://i.imgur.com/tHmqRkk.png)