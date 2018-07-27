# warframe_market_extraction
Searches warframe.market for item inputs and returns platinum values in a csv

### How to use
1. Create and fill out input.csv, entries should be all lower case with underscores replacing spaces
one entry per line.
2. Run warframe_market_extractor.py and wait for it to fill out the entries in output.csv.
3. Import the output.csv into a spreadsheet tool and do whatever you want with the results.

### Dependancies
BeautifulSoup4
install via pip
```
pip install beautifulsoup4
```

### Input.csv
```
akbolto_prime_barrel
carrier_prime_cerebrum
legendary_fusion_core
```

### Output.csv
| Item                   | Buy Value     | Sell Value  |
| ---------------------- |:-------------:| -----------:|
| akbolto_prime_barrel   | 3p            | 2p          |
| carrier_prime_cerebrum | 61p           | 75p         |
| legendary_fusion_core  | 280p          | 325p        |
