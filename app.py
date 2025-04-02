from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from transport_company import TransportCompany

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Для безпеки сесій
company = TransportCompany()

# Підключення до бази
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Головна сторінка
@app.route('/')
def index():
    return render_template('index.html')

# Реєстрація нового користувача
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Перевірка, чи є такий користувач
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Користувач вже існує!', 'danger')
        else:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            flash('Реєстрація успішна! Тепер увійдіть.', 'success')
            return redirect(url_for('login'))

        conn.close()

    return render_template('templates_register.html')

# Вхід користувача
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Невірний логін або пароль!', 'danger')

    return render_template('templates_login.html')

# Особистий кабінет
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('templates_dashboard.html', username=session['username'])

# Вихід
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
