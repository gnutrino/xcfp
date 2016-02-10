XCom Character File Parser
==========================

This is a quick python library I cooked up for parsing character data out of
the character pool files for XCOM 2

Usage
-----

The main class for this libray is CharacterPool, 

```python
from xcfp.lib import CharacterPool

pool = CharacterPool('/path/to/file.bin'):
for char in pool.characters():
	print(char)
```
