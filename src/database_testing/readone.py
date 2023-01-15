#!/usr/bin/env python3
import argparse
import logging
import os
import random
import time
import uuid
from database_testing import _DBNAME
import sqlite3
total_added = 0

conn = sqlite3.connect(_DBNAME)
cur = conn.cursor()
# noinspection SqlResolve
cur.execute("select count(*) from somedata")
r = cur.fetchone()
nrows = r[0]
test_row = random.randrange(nrows)
print(f"testing {test_row} of {nrows}")
# noinspection SqlResolve
cur.execute(f"select uuid from somedata where rowid = {test_row}")
r = cur.fetchone()
fuuid = r[0]
start = time.perf_counter()
# noinspection SqlResolve
cur.execute(f"select blob from somedata where uuid = '{fuuid}'")
r = cur.fetchone()
stop = time.perf_counter()
print(f"Found {r[0]} for {fuuid} in {stop - start} seconds")




