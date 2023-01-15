#!/usr/bin/env python3
import argparse
import logging
import os
import uuid
from database_testing import _DBNAME
import sqlite3
total_added = 0

def dbsize():
    return os.stat(_DBNAME).st_size

def add_some(conn,n):
    global  total_added
    conn.commit()
    before = dbsize()
    cur = conn.cursor()
    for i in range(int(n)):
        ident = uuid.uuid4()
        data = f"somedata{i:010}"
        cur.execute(f"""INSERT INTO somedata VALUES('{ident}','{data}')""")
    total_added += int(n)
    conn.commit()
    after = dbsize()
    return after - before



parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('size',type=int)
args = parser.parse_args()
try:
    os.unlink(_DBNAME)
except:
    pass
conn = sqlite3.connect(_DBNAME)
cur = conn.cursor()
cur.execute("CREATE TABLE somedata(uuid,blob)")
adding = 1
while (increase := add_some(conn,adding)) == 0:
    adding+=1
print(f'{total_added} {adding} {increase}')
size_per_row = increase / total_added
to_add = (args.size - dbsize()) / size_per_row

while dbsize() < args.size:
    print(f"{dbsize()} {args.size} {to_add}")
    increase = add_some(conn,to_add)
    size_per_row = increase / to_add
    to_add = (args.size - dbsize()) / size_per_row



