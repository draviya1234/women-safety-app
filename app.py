from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session, g
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('site.db')
        g.db.row_factory = sqlite3.Row
    return g.db

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Check if the username already exists
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            flash('Username already exists. Please choose a different one.', 'error')
            conn.close()
            return redirect(url_for('signup'))

        # Use the default hashing method
        hashed_password = generate_password_hash(password)

        # Insert the new user into the database
        cursor.execute('INSERT INTO users (username, password, user_type) VALUES (?, ?, ?)',
                       (username, hashed_password, user_type))
        conn.commit()
        conn.close()

        flash('Account created successfully. Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Check if the username exists
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(user[2], password):
            flash('Login successful!', 'success')
            session['user_type'] = user[3]
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('dashboard', user_type=user[3]))
        else:
            flash('Login failed. Check your username and password.', 'error')

    return render_template('login.html')


# Default route with navbar
@app.route('/game')
def game():
    return render_template('game.html')



if __name__ == '__main__':
    app.run(debug=True)