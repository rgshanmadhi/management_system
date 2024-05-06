from flask import Flask, request, render_template, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'

def init_db():
    with sqlite3.connect(DATABASE) as db:
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')
        db.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        print("GET request received for /users")
        db = get_db()
        cursor = db.execute('SELECT * FROM users')
        users = cursor.fetchall()
        db.close()
        return jsonify(users)
    elif request.method == 'POST':
        data = request.json
        name = data.get('name')
        email = data.get('email')
        print("POST request received for /users")
        print(f"Name: {name}, Email: {email}")
        db = get_db()
        db.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
        db.commit()
        db.close()
        return jsonify({'message': 'User added successfully'})

def get_db():
    db = sqlite3.connect(DATABASE)
    return db

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
