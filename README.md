XCom Character File Parser
==========================

This is a quick python library I cooked up for parsing character data out of
the character pool files for XCOM 2

Usage
-----

The main class for this libray is CharacterPool, 

```python
from xcfp.lib import CharacterPool

with CharacterPool('/path/to/file.bin') as pool:
	pool.read_header()
    print("Number of characters in file: {}".format(pool.count))

	for char in pool.characters():
		print(char)
```
