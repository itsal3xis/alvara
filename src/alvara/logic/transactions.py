import sqlite3
import math
import time
from account import account
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "alvara.db")


def balance_calculation(transaction_id, card):
    conn = sqlite3.connect(account.DB_PATH)
    cursor = conn.cursor()

    # Get the transaction details
    cursor.execute('''
        SELECT amount, transaction_type FROM transactions WHERE id = ?
    ''', (transaction_id,))
    transaction = cursor.fetchone()

    if transaction:
        amount, transaction_type = transaction
        if transaction_type == "debit":
            cursor.execute('''
                UPDATE cards SET balance = balance - ? WHERE card_number = ?
            ''', (amount, card))
        elif transaction_type == "credit":
            cursor.execute('''
                UPDATE cards SET balance = balance + ? WHERE card_number = ?
            ''', (amount, card))
        conn.commit()
    conn.close()





class Transaction:
    def __init__(self, id, sender, receiver, amount, transaction_type, card, date=time.strftime("%Y-%m-%d %H:%M:%S")):
        self.transaction_id = id
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.transaction_type = transaction_type
        self.card = card
        self.date = date if date else time.strftime("%Y-%m-%d %H:%M:%S")

    def save_to_db(self):
        conn = sqlite3.connect(account.DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transactions (transaction_id, sender, receiver, amount, transaction_type, card, date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (self.transaction_id, self.sender, self.receiver, self.amount, self.transaction_type, self.card, self.date))
        conn.commit()
        conn.close()


