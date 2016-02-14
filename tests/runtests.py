#!/usr/bin/python3

import unittest as ut
from unittest import defaultTestLoader as loader
import pkgutil
import os, sys

TEST_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(TEST_DIR, os.pardir))

sys.path.append(ROOT_DIR)

if __name__ == "__main__":
    suites = []
    for _, name, _ in pkgutil.iter_modules([TEST_DIR]):
        if not name.startswith('test'):
            continue
        suites.append(loader.loadTestsFromName(name))

    runner = ut.TextTestRunner(verbosity=2)
    for suite in suites:
        runner.run(suite)
