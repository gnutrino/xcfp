#!/usr/bin/python3
from struct import pack,unpack
from lib import CharacterPool

if __name__ == "__main__":
    from sys import argv
    if len(argv) < 2:
        print("Usage: {} character_file".format(argv[0]))
        exit(1)

    with CharacterPool(argv[1]) as pool:
        for char in pool.characters():
            print(char)
