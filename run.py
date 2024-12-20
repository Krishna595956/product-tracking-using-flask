from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For flash messages

# MongoDB connection
client = MongoClient("mongodb+srv://krishnareddy:1234567890@diploma.1v5g6.mongodb.net/")
db = client['farmconnect']
users_collection = db['users']

# Helper function to handle password hashing
def hash_password(password):
    return generate_password_hash(password)

@app.route('/')
def index():
    return render_template('index.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        if not name or not email or not password or not role:
            flash('All fields are required!', 'danger')
            return redirect(url_for('register'))
        
        existing_user = users_collection.find_one({"email": email})
        if existing_user:
            flash('Email already exists!', 'danger')
            return redirect(url_for('register'))

        hashed_password = hash_password(password)
        new_user = {
            'name': name,
            'email': email,
            'password': hashed_password,
            'role': role
        }

        users_collection.insert_one(new_user)
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')  # Render the registration form

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Please provide both email and password!', 'danger')
            return redirect(url_for('login'))

        user = users_collection.find_one({"email": email})
        if not user or not check_password_hash(user['password'], password):
            flash('Invalid email or password!', 'danger')
            return redirect(url_for('login'))

        flash('Login successful!', 'success')
        return redirect(url_for('dashboard'))  # Redirect to user dashboard

    return render_template('login.html')  # Render the login form

if __name__ == '__main__':
    app.run(debug=True)
