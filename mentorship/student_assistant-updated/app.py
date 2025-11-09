from flask import Flask, request, redirect, session, render_template, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# ---------------------- DATABASE INIT ----------------------
def init_db():
    if not os.path.exists('users.db'):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

init_db()

# ---------------------- ROUTES ----------------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        print(f"Message from {name} ({email}): {message}")
        flash('Thanks for contacting us! We\'ll get back to you soon.', 'success')
        return redirect('/contact')
    return render_template('contact.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/under-construction')
def under_construction():
    return render_template('under-construction.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if 'user' in session:
        return redirect('/features')
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['user'] = user[1]
            return redirect('/features')
        else:
            flash('Invalid email or password. Please try again.', 'error')
            return redirect('/signin')
    return render_template('signin.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user' in session:
        return redirect('/features')
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        try:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
            conn.commit()
            conn.close()
            flash('Account created successfully! Please sign in.', 'success')
            return redirect('/features')
        except sqlite3.IntegrityError:
            flash('Email already registered. Please sign in.', 'error')
            return redirect('/signin')
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out successfully.', 'success')
    return redirect('/signin')

# ---------------------- RUN APP ----------------------
if __name__ == '__main__':
    app.run(debug=True)
