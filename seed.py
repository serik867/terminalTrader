import sqlite3
import hashlib
from model import SALT
import time

def run(dbname="ttrader.db"):
    conn = sqlite3.connect(dbname)
    cur  = conn.cursor()

    hasher = hashlib.sha512()
    hasher.update((SALT + 'password!').encode('utf-8'))
    pass_hash = hasher.hexdigest()

    SQL = """INSERT INTO accounts 
        (username, firstname, lastname, account_type, 
        account_id, pass_hash, balance) 
        VALUES
        (?, ?, ?, ?, ?, ?, ?); """

    cur.execute(SQL, ('carter', 'Carter', 'Adams', 'Admin',
                    '000001', pass_hash, 10000.00))

    SQL = """INSERT INTO accounts 
        (username, firstname, lastname, account_type, 
        account_id, pass_hash, balance) 
        VALUES
        (?, ?, ?, ?, ?, ?, ?); """

    cur.execute(SQL, ('sero', 'ser', 'dudu', 'User',
                     '000002', pass_hash, 10000.00))

    SQL = """ INSERT INTO positions
        (account_pk, symbol, amount)
         VALUES
        (?, ?, ?); """

    cur.execute(SQL, (1, 'tsla', 5))

    SQL = """ INSERT INTO trades
        (account_pk, symbol, volume, price, time)
        VALUES
        (?, ?, ?, ?, ?); """

    cur.execute(SQL, (1, 'tsla', 5, 100.00, int(time.time())))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    run()