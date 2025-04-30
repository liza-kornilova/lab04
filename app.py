from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

# Инициализация приложения
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secret123'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Модель пользователя
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(10), nullable=False, default="client")  # client или admin

# Загрузка пользователя Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# О компании
@app.route('/about')
def about():
    return render_template('about.html')

# Услуги
@app.route('/services')
def services():
    return render_template('services.html')

# Контакты
@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        
      
        
        flash('Спасибо за обращение! Мы свяжемся с вами в ближайшее время.', 'success')
        return redirect(url_for('contacts'))
        
    return render_template('contacts.html')

# Регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        
        if User.query.filter_by(username=username).first():
            flash('Такой логин уже существует!', 'danger')
            return redirect(url_for('register'))
            
        new_user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Регистрация успешна! Теперь войдите.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

# Вход
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Неверный логин или пароль!', 'danger')
            
    return render_template('login.html')

# Личный кабинет
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

# Выход
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из учетной записи', 'info')
    return redirect(url_for('index'))

# Запуск приложения
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создает базу данных при первом запуске
    app.run(debug=True)
