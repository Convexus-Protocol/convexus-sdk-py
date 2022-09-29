## Swap price impact

Compute the price impact from a given swap

### Install
```bash
$ python -m venv venv
$ source ./venv/bin/activate
$ pip install -r ./examples/swap-price-impact/requirements.txt
```

### Usage

```bash
$ python ./examples/swap-price-impact <pool address> <token symbol to swap> <amount to swap>
```

### Example

```bash
# Swap 10 WETH (10 * 10**18) in the WETH/CRV pool
python ./examples/swap-price-impact cx504c9900b3964dacbbdb3daaedbcc8e0cc070f94 WETH 10000000000000000000
```

```bash
Price before = 1364 WETH/CRV
Price after  = 1318.9637 WETH/CRV
```