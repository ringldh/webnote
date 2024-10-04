from flask import Flask, request, jsonify, render_template
import sqlite3
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Database file path
DATABASE = 'notes.db'

# Initialize the database if it doesn't exist
def init_db():
    """Initializes the database if it doesn't exist."""
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

# Helper function to get database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Route for loading the webpage
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint to load the latest note
@app.route('/load', methods=['GET'])
def load_note():
    conn = get_db_connection()
    note = conn.execute('SELECT content FROM notes ORDER BY timestamp DESC LIMIT 1').fetchone()
    conn.close()
    if note:
        return jsonify({'content': note['content']})
    else:
        return jsonify({'content': ''})

# API endpoint to save the note
@app.route('/save', methods=['POST'])
def save_note():
    content = request.json.get('content')
    conn = get_db_connection()
    conn.execute('INSERT INTO notes (content) VALUES (?)', (content,))
    conn.commit()
    conn.close()
    print('Note saved!')
    return jsonify({'message': 'Note saved!'})

if __name__ == '__main__':
    init_db()  # Initialize the database when the app starts
    app.run(debug=True)
