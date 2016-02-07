#!/usr/bin/python3
from struct import pack,unpack
from lib import CharacterPool

if __name__ == "__main__":
    from sys import argv
    if len(argv) < 2:
        print("Usage: {} character_file".format(argv[0]))
        exit(1)

    pool = CharacterPool(argv[1])
    for char in pool.characters():
        print(char)
