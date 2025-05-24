from flask import Flask, request, jsonify
import os
import sys

# Pour importer le module account correctement
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from alvara.logic.account import account

app = Flask(__name__)

@app.route('/api/accounts', methods=['GET'])
def get_accounts(id_account):
    # Exemple : retourne tous les comptes (à adapter selon ta structure)
    conn = account.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, fname, lname, age, address, phone, email FROM accounts WHERE id = ?", (id_account,))
    accounts = [
        dict(zip(['id', 'fname', 'lname', 'age', 'address', 'phone', 'email'], row))
        for row in cursor.fetchall()
    ]
    conn.close()
    return jsonify(accounts)

@app.route('/api/accounts', methods=['POST'])
def create_account():
    data = request.json
    try:
        new_account = account(
            data['fname'],
            data['lname'],
            int(data['age']),
            data['address'],
            data['password'],
            data['phone'],
            data['email'],
            cards=[]
        )
        return jsonify({"message": "Account created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    account.init_db()  # S'assure que la base existe
    app.run(debug=True, port=5001)
