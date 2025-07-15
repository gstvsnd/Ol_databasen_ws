from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__, instance_relative_config=True)

# Skapa databas om den inte finns
db_path = os.path.join(app.instance_path, 'beer.db')
os.makedirs(app.instance_path, exist_ok=True)

def init_db():
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS beers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                brewery TEXT NOT NULL,
                competition TEXT NOT NULL
            )
        ''')
        conn.commit()

# Initiera databasen
init_db()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)