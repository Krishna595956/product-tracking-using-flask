from flask import Flask, render_template, request, redirect, url_for, flash,session
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For flash messages

# MongoDB connection
client = MongoClient("")
db = client['farmconnect']
users_collection = db['users']
products_collection = db['products']

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
        session['email'] = email

        flash('Login successful!', 'success')
        return redirect(url_for('dashboard'))  # Redirect to user dashboard

    return render_template('login.html')  # Render the login form

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/addproduct")
def addproduct():
    return render_template("addProduct.html")

@app.route('/addproduct', methods=['POST'])
def add_product():
    # Get form data from the POST request
    crop_name = request.form.get('crop_name')
    crop_type = request.form.get('crop_type')
    growth_stage = request.form.get('growth_stage')
    pest_status = request.form.get('pest_status')
    soil_condition = request.form.get('soil_condition')
    harvest_prediction = request.form.get('harvest_prediction')
    temperature_range = request.form.get('temperature_range')
    humidity = request.form.get('humidity')
    fertilizers_used = request.form.get('fertilizers_used')
    pest_control_methods = request.form.get('pest_control_methods')
    yield_prediction = request.form.get('yield_prediction')
    challenges_faced = request.form.get('challenges_faced')
    additional_notes = request.form.get('additional_notes')

    # Convert the harvest prediction to a date object
    try:
        harvest_date = datetime.strptime(harvest_prediction, '%Y-%m-%d')
    except ValueError:
        flash('Invalid harvest prediction date format!', 'danger')
        return redirect(url_for('addproduct'))

    # Create the product document
    new_product = {
        'crop_name': crop_name,
        'crop_type': crop_type,
        'growth_stage': growth_stage,
        'pest_status': pest_status,
        'soil_condition': soil_condition,
        'harvest_prediction': harvest_date,
        'temperature_range': temperature_range,
        'humidity': humidity,
        'fertilizers_used': fertilizers_used,
        'pest_control_methods': pest_control_methods,
        'yield_prediction': yield_prediction,
        'challenges_faced': challenges_faced,
        'additional_notes': additional_notes
    }

    products_collection.insert_one(new_product)

    # Flash a success message and redirect to a confirmation page
    flash('Product added successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/products')
def display_products():
    products = list(products_collection.find())
    return render_template('products.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
