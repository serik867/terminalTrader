from json.decoder import JSONDecodeError
import requests
import opencursor
import time
from opencursor import OpenCursor
import hashlib
from random import randint

API_URL = "https://api.iextrading.com/1.0/stock/{symbol}/quote"
opencursor.setDB('ttrader.db')

ACCOUNT_ID_DIGITS = 10
SALT = "SECRET SALT"

#hash the string for password
def hash_string(string):
    hasher = hashlib.sha512()
    hasher.update((SALT + string).encode('utf-8'))
    return hasher.hexdigest()

#look price by go to the symbol url and
#return result in json file and the lastPrice
def lookup_price(symbol):
    try:
        result = requests.get(API_URL.format(symbol=symbol))
        return result.json()['latestPrice']
    except JSONDecodeError:
        raise ValueError("Symbol not found")

#generate id number from 10**9 to (10**9)-1
def generate_id_number():
    minimum = 10 ** (ACCOUNT_ID_DIGITS - 1)
    maximum = (10 ** ACCOUNT_ID_DIGITS) - 1
    return randint(minimum, maximum)

#check existed of id and return bool - True or False and
#go to the request from sqllite3
def id_exists(idnum):
    with OpenCursor() as cur:
        SQL = "SELECT pk FROM accounts WHERE account_id = ?;"
        cur.execute(SQL, (idnum,))
        row = cur.fetchone()
    return bool(row)

#genearate new id and check from databasa if there that id 
#then new id generate until there no that id in database
def new_id_num():
    newid = generate_id_number()
    while id_exists(newid):
        newid = generate_id_number()
    return newid

class Account:
# initiate class from credentials or empty
    def __init__(self, row={}, username='', password=''):
        if username:
            self._set_from_credentials(username, password)
        else:
            self._set_from_row(row)

#iniate row with varaubles...
    def _set_from_row(self, row):
        row = dict(row)
        self.pk = row.get('pk')
        self.username = row.get('username')
        self.firstname = row.get('firstname')
        self.lastname = row.get('lastname')
        self.account_id = row.get('account_id')
        self.pass_hash = row.get('pass_hash')
        self.balance = row.get('balance', 0.0)

#find account from username and ppassword if not exist account 
#then empty row
    def _set_from_credentials(self, username, password):
        pass_hash = hash_string(password)
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM accounts WHERE
                username = ? AND pass_hash = ?; """
            cur.execute(SQL, (username, pass_hash))
            row = cur.fetchone()
        if row:
            self._set_from_row(row)
        else:
            self._set_from_row({})

#set new account_id by use function called new_id_num()
    def set_new_id(self):
        self.account_id = new_id_num()

#hash the password for that us hash_string()
    def set_hashed_password(self, password):
        self.pass_hash = hash_string(password)

#account save if not exist or update 
    def save(self):
        if self:
            with OpenCursor() as cur:
                SQL = """ UPDATE accounts SET 
                    username = ?, firstname = ?, lastname = ?,
                    account_id = ?, pass_hash = ?, balance = ?
                    WHERE pk=?; """
                values = (self.username, self.firstname, self.lastname,
                          self.account_id, self.pass_hash, self.balance,
                          self.pk)
                cur.execute(SQL, values)
        else:
            with OpenCursor() as cur:
                SQL = """ INSERT INTO accounts (
                    username, firstname, lastname,
                    account_id, pass_hash, balance)
                    VALUES (
                    ?, ?, ?, ?, ?, ?); """
                values = (self.username, self.firstname, self.lastname,
                          self.account_id, self.pass_hash, self.balance)
                cur.execute(SQL, values)
                self.pk = cur.lastrowid

#get postion from database by list of positions
    def get_positions(self):
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM positions WHERE account_pk = ?; """
            cur.execute(SQL, (self.pk,))
            rows = cur.fetchall()
        return [Position(row) for row in rows]

#get from database and show cur.fetchone()on Position(row)
    def get_position(self, symbol):
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM positions WHERE
                    account_pk = ? AND symbol = ?; """
            cur.execute(SQL, (self.pk, symbol))
            row = cur.fetchone()
        if row:
            return Position(row)

        newposition = Position()
        newposition.account_pk = self.pk
        newposition.symbol = symbol
        newposition.amount = 0
        return newposition

#get trades from database and show the fetchall() 
    def get_trades(self):
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM trades WHERE 
                account_pk = ? ORDER BY time DESC; """
            cur.execute(SQL, (self.pk,))
            rows = cur.fetchall()

        return [Trade(row) for row in rows]

#get trades for special symbool
    def get_trades_for(self, symbol):
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM trades WHERE
                account_pk = ? AND symbol = ?
                ORDER BY time DESC; """
            cur.execute(SQL, (self.pk, symbol))
            rows = cur.fetchall()

        return [Trade(row) for row in rows]

#increase position and increase the amount
    def increase_position(self, symbol, amount):
        pos = self.get_position(symbol)
        pos.amount += amount
        pos.save()

#get position and decrease the amount
    def decrease_position(self, symbol, amount):
        pos = self.get_position(symbol)
        if pos.amount < amount:
            raise ValueError("Not enough shares held")
        pos.amount -= amount
        pos.save()

#make trade and save it
    def make_trade(self, symbol, volume, price):
        trade = Trade()
        trade.account_pk = self.pk
        trade.symbol = symbol
        trade.volume = volume
        trade.price = price
        trade.save()

#buy first take price from look_up price than check balance 
#that amount multiple by price if it greater than balance do it
    def buy(self, symbol, amount, price=None):
        if not price:
            price = lookup_price(symbol)
        if self.balance < amount * price:
            raise ValueError("Insufficient Funds")
        self.increase_position(symbol, amount)
        self.make_trade(symbol, amount, price)
        self.balance -= amount * price
        self.save()

#loo_up price then decrease_position 
    def sell(self, symbol, amount, price=None):
        if not price:
            price = lookup_price(symbol)
        self.decrease_position(symbol, amount)
        self.make_trade(symbol, -amount, price)
        self.balance += amount * price
        self.save()
        
#built in function that check is instance exist in database
    def __bool__(self):
        return bool(self.pk)

#show acount like that
    def __repr__(self):
        output = "<Account {}, {}>".format(self.pk, self.username)
        return output


class Position:
#iniate Position classs (pk,account pk,symbol,amount)
    def __init__(self, row={}):
        row = dict(row)
        self.pk = row.get('pk')
        self.account_pk = row.get('account_pk')
        self.symbol = row.get('symbol')
        self.amount = row.get('amount')

#save Postion either exist or not exist than create one
    def save(self):
        if self:
            with OpenCursor() as cur:
                SQL = """ UPDATE positions SET 
                    account_pk = ?, symbol = ?, amount = ?
                    WHERE pk=?; """
                values = (self.account_pk, self.symbol, self.amount, self.pk)
                cur.execute(SQL, values)

        else:
            with OpenCursor() as cur:
                SQL = """ INSERT INTO positions (
                    account_pk, symbol, amount)
                    VALUES (?, ?, ?); """
                values = (self.account_pk, self.symbol, self.amount)
                cur.execute(SQL, values)
                self.pk = cur.lastrowid

#get price that symbol
    def get_value(self):
        price = lookup_price(self.symbol)
        return self.amount * price

#check object exist or not
    def __bool__(self):
        return bool(self.pk)

    def __repr__(self):
        output = "<Position_pk: {}, account_pk: {}, symbol: {}, amount: {}>"
        return output.format(self.pk, self.account_pk, self.symbol, self.amount)


class Trade:
    def __init__(self, row={}):
        row = dict(row)
        self.pk = row.get("pk")
        self.account_pk = row.get("account_pk")
        self.symbol = row.get("symbol")
        self.volume = row.get("volume")
        self.price = row.get("price")
        self.time = row.get("time")

    def save(self):
        if self:
            with OpenCursor() as cur:
                SQL = """ UPDATE trades SET 
                    account_pk = ?, symbol = ?, volume = ?,
                    price = ?, time = ?
                    WHERE pk=?; """
                values = (self.account_pk, self.symbol, self.volume,
                          self.price, self.time, self.pk)
                cur.execute(SQL, values)

        else:
            if not self.time:
                self.time = int(time.time())

            with OpenCursor() as cur:
                SQL = """ INSERT INTO trades (
                    account_pk, symbol, volume, price, time)
                    VALUES (?, ?, ?, ?, ?); """
                values = (self.account_pk, self.symbol, self.volume,
                          self.price, self.time)
                cur.execute(SQL, values)
                self.pk = cur.lastrowid

    def __bool__(self):
        return bool(self.pk)

    def __repr__(self):
        output = "<Trade pk: {}, account_pk: {}, symbol: {}, volume: {}, price: {},time: {}>"
        return output.format(self.pk, self.account_pk, self.symbol, self.volume, self.price, self.time)
