import sqlite3
import os

class account:
    # Chemin absolu vers le dossier logic
    DB_PATH = os.path.join(os.path.dirname(__file__), "alvara.db")

    @staticmethod
    def init_db():
        conn = sqlite3.connect(account.DB_PATH)
        cursor = conn.cursor()
        # Table des comptes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fname TEXT,
                lname TEXT,
                age INTEGER,
                address TEXT,
                password TEXT,
                phone TEXT,
                email TEXT
            )
        ''')
        # Table des cartes liées à un compte
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                card_number TEXT,
                card_type TEXT,
                balance REAL,
                account_id INTEGER,
                FOREIGN KEY(account_id) REFERENCES accounts(id)
            )
        ''')
        conn.commit()
        conn.close()

    @staticmethod
    def get_connection():
        return sqlite3.connect(account.DB_PATH)

    def verify_age(self, age):
        if age < 16:
            raise ValueError("Age must be at least 16")
        return age

    def encrypt_password(self, password):
        # Placeholder for password encryption logic
        return password

    def phone_verify(self, phone):
        if len(phone) != 10 or not phone.isdigit():
            raise ValueError("Phone number must be 10 digits")
        return phone

    def email_verify(self, email):
        if "@" not in email or "." not in email:
            raise ValueError("Invalid email address")
        return email

    def __init__(self, fname, lname, age, address, password, phone, email, cards=None):
        self.fname = fname[0].upper() + fname[1:]
        self.lname = lname[0].upper() + lname[1:]
        self.age = self.verify_age(age)
        self.address = address
        self.password = self.encrypt_password(password)
        self.phone = self.phone_verify(phone)
        self.email = self.email_verify(email)
        self.cards = cards if cards is not None else []

        self.account_id = self.save_to_db()
        self.save_cards_to_db()

    def save_to_db(self):
        conn = sqlite3.connect(account.DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO accounts (fname, lname, age, address, password, phone, email)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (self.fname, self.lname, self.age, self.address, self.password, self.phone, self.email))
        conn.commit()
        account_id = cursor.lastrowid
        conn.close()
        return account_id

    def save_cards_to_db(self):
        if not self.cards:
            return
        conn = sqlite3.connect(account.DB_PATH)
        cursor = conn.cursor()
        for card in self.cards:
            cursor.execute('''
                INSERT INTO cards (card_number, card_type, balance, account_id)
                VALUES (?, ?, ?, ?)
            ''', (card['card_number'], card['card_type'], card['balance'], self.account_id))
        conn.commit()
        conn.close()

    def __str__(self):
        return f"Account({self.fname}, {self.lname}, {self.age}, {self.address}, {self.password}, {self.phone}, {self.email}, {self.cards})"

# Initialiser la base de données (à appeler une fois au démarrage de l'app)
account.init_db()

