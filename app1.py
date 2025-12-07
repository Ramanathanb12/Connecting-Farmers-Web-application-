from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import bcrypt
from flask import jsonify
from datetime import datetime
import random
import os

app = Flask(__name__)

# Configure SQLite database
app.config['DATABASE'] = 'registration_dbs.db'
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize database function
def get_db():
    db = sqlite3.connect(app.config['DATABASE'])
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        # Create users table
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                location TEXT,
                phone TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')
        
        # Create farmer table
        db.execute('''
            CREATE TABLE IF NOT EXISTS farmer (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                farmer_name TEXT NOT NULL,
                crops_grown TEXT NOT NULL,
                rate_per_kg REAL NOT NULL,
                available_kgs INTEGER NOT NULL,
                location TEXT NOT NULL,
                phone TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create market table
        db.execute('''
            CREATE TABLE IF NOT EXISTS market (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                market_name TEXT NOT NULL,
                available_goods TEXT NOT NULL,
                price_per_unit REAL NOT NULL,
                market_location TEXT NOT NULL,
                phone TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create messages table
        db.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_id INTEGER NOT NULL,
                recipient_id INTEGER NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                is_read BOOLEAN DEFAULT 0,
                name TEXT,
                FOREIGN KEY (sender_id) REFERENCES users (id),
                FOREIGN KEY (recipient_id) REFERENCES users (id)
            )
        ''')
        
        # Create orders table
        db.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                market_name TEXT,
                quantity_kg INTEGER,
                total_price REAL,
                farmer_name TEXT,
                payment_method TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        db.commit()

# Initialize the database when the app starts
if not os.path.exists(app.config['DATABASE']):
    init_db()

# Global variable for alerts
farmer_alerts = []
market_alerts = []

# Route for Home Page
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/gov_schems')
def gov_schems():
    return render_template('gov_schems.html')

# Chatbot functionality
import google.generativeai as genai

# Configure API key
genai.configure(api_key="AIzaSyClwCo8aIpV8gieeDQ5HsjiASODhGkxt-0")

# Generation settings
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Create the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="You are a chatbot to help users with farmer details and all marketing-related topics."
)

# Start the chat session
chat_session = model.start_chat()

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form.get('user_input')
    if not user_input:
        return jsonify({'response': "I didn't quite understand that. Can you please rephrase?"})

    # Send user message to the chat session
    response = chat_session.send_message(user_input)
    
    # Return bot's response as a JSON object
    return jsonify({'response': response.text})

# Route for Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        phone = request.form['phone']
        password = request.form['password']
        role = request.form['role']

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        db = get_db()
        try:
            db.execute("INSERT INTO users (name, location, phone, password, role) VALUES (?, ?, ?, ?, ?)", 
                      (name, location, phone, hashed_password.decode('utf-8'), role))
            db.commit()
            flash("You have successfully registered! Please log in.", 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Phone number already exists!", 'danger')
            return redirect(url_for('register'))
        except Exception as e:
            flash(f"An error occurred: {str(e)}", 'danger') 
            return redirect(url_for('register'))
        finally:
            db.close()
    return render_template('register.html')

# Route for Login Page
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         phone = request.form['phone']
#         password = request.form['password']

#         db = get_db()
#         user = db.execute("SELECT * FROM users WHERE phone = ?", (phone,)).fetchone()

#         if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
#             session['user_id'] = user['id']
#             session['user_name'] = user['name']
#             session['user_role'] = user['role']
#             flash("Login successful!", 'success')

#             if user['role'] == 'farmer':
#                 return redirect(url_for('farmer_dashboard'))
#             else:
#                 return redirect(url_for('market_dashboard'))
#         else:
#             flash("Incorrect phone number or password.", 'danger')
#             return redirect(url_for('login'))
#         db.close()
#     return render_template('login.html')

# this is ur code 
# -----------------------------------------------------------------
# this is my code 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']

        db = get_db()
        try:
            user = db.execute("SELECT * FROM users WHERE phone = ?", (phone,)).fetchone()

            if user:
                stored_password = user['password']
                user_role = user['role'].strip().lower()  # Normalize role

                # Debug logs
                print("User found:", user['name'], "| Role:", user_role)

                if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                    session['user_id'] = user['id']
                    session['user_name'] = user['name']
                    session['user_role'] = user_role
                    flash("Login successful!", 'success')

                    if user_role == 'farmer':
                        return redirect(url_for('farmer_dashboard'))
                    elif user_role == 'market':
                        return redirect(url_for('market_dashboard'))
                    else:
                        flash("Invalid user role. Please contact admin.", 'danger')
                        return redirect(url_for('login'))
                else:
                    flash("Incorrect password.", 'danger')
            else:
                flash("Phone number not found.", 'danger')
        except Exception as e:
            print("Login error:", str(e))
            flash("Something went wrong during login.", 'danger')
        finally:
            db.close()
        
        return redirect(url_for('login'))

    return render_template('login.html')



# -----------------------------------------------------------------
from datetime import datetime

# Route for Farmer Dashboard
# @app.route('/farmer_dashboard', methods=['GET', 'POST'])
# def farmer_dashboard():
#     if 'user_id' not in session:
#         flash("You must log in first!", 'danger')
#         return redirect(url_for('login'))

#     if request.method == 'POST':
#         user_id = session['user_id']
#         farmer_name = request.form['farmer_name']
#         crops_grown = request.form['crops_grown']
#         available_kgs = int(request.form['available_kgs'])
#         location = request.form['location']
#         phone = request.form['phone']

       
#         if available_kgs == 1:
#             rate_per_kg = round(random.uniform(25, 100), 2)  
#         elif available_kgs > 1000:
#             rate_per_kg = round(random.uniform(200, 300), 2)  
#         else:
#             rate_per_kg = round(random.uniform(100, 200), 2)  
        
#         # Insert into the database
#         db = get_db()
#         db.execute(
#             "INSERT INTO farmer (user_id, farmer_name, crops_grown, rate_per_kg, available_kgs, location, phone) VALUES (?, ?, ?, ?, ?, ?, ?)",
#             (user_id, farmer_name, crops_grown, rate_per_kg, available_kgs, location, phone)
#         )
#         db.commit()
#         db.close()
#         flash("Farmer details submitted successfully!", 'success')

#     # Check for new messages and convert timestamps
#     db = get_db()
#     new_messages = db.execute(
#         "SELECT * FROM messages WHERE recipient_id = ? AND is_read = 0",
#         (session['user_id'],)
#     ).fetchall()

#     # Convert message timestamp strings to datetime objects
#     formatted_messages = []
#     for msg in new_messages:
#         msg_dict = dict(msg)
#         try:
#             msg_dict['timestamp'] = datetime.strptime(msg_dict['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
#         except ValueError:
#             msg_dict['timestamp'] = datetime.strptime(msg_dict['timestamp'], '%Y-%m-%d %H:%M:%S')
#         formatted_messages.append(msg_dict)

#     db.close()

#     return render_template('farmer_dashboard.html', messages=formatted_messages)
from datetime import datetime
import random  # Don't forget to import random if it's not already

@app.route('/farmer_dashboard', methods=['GET', 'POST'])
def farmer_dashboard():
    if 'user_id' not in session:
        flash("You must log in first!", 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        user_id = session['user_id']
        farmer_name = request.form['farmer_name']
        crops_grown = request.form['crops_grown']
        available_kgs = int(request.form['available_kgs'])
        location = request.form['location']
        phone = request.form['phone']

        # 🔄 Always generate rate_per_kg between 50 and 100
        rate_per_kg = round(random.uniform(50, 100), 2)

        # Insert into the database
        db = get_db()
        db.execute(
            "INSERT INTO farmer (user_id, farmer_name, crops_grown, rate_per_kg, available_kgs, location, phone) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user_id, farmer_name, crops_grown, rate_per_kg, available_kgs, location, phone)
        )
        db.commit()
        db.close()
        flash("Farmer details submitted successfully!", 'success')

    # Check for new messages and convert timestamps
    db = get_db()
    new_messages = db.execute(
        "SELECT * FROM messages WHERE recipient_id = ? AND is_read = 0",
        (session['user_id'],)
    ).fetchall()

    # Format timestamps
    formatted_messages = []
    for msg in new_messages:
        msg_dict = dict(msg)
        try:
            msg_dict['timestamp'] = datetime.strptime(msg_dict['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            msg_dict['timestamp'] = datetime.strptime(msg_dict['timestamp'], '%Y-%m-%d %H:%M:%S')
        formatted_messages.append(msg_dict)

    db.close()

    return render_template('farmer_dashboard.html', messages=formatted_messages)


# Route for Market Dashboard
from datetime import datetime

@app.route('/market_dashboard', methods=['GET', 'POST'])
def market_dashboard():
    if 'user_id' not in session:
        flash("You must log in first!", 'danger')
        return redirect(url_for('login'))

    db = get_db()
    
    # Fetch all products
    products = db.execute("SELECT * FROM farmer").fetchall()

    # Fetch unread messages
    raw_messages = db.execute("SELECT * FROM messages WHERE recipient_id = ? AND is_read = 0", (session['user_id'],)).fetchall()

    # Format messages to convert timestamp to datetime
    formatted_messages = []
    for msg in raw_messages:
        msg_dict = dict(msg)
        try:
            msg_dict['timestamp'] = datetime.strptime(msg_dict['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            msg_dict['timestamp'] = datetime.strptime(msg_dict['timestamp'], '%Y-%m-%d %H:%M:%S')
        formatted_messages.append(msg_dict)

    if request.method == 'POST':
        user_id = session['user_id']
        market_name = request.form['market_name']
        available_goods = request.form['available_goods']
        price_per_unit = request.form['price_per_unit']
        market_location = request.form['market_location']
        phone = request.form['phone']

        db.execute("INSERT INTO market (user_id, market_name, available_goods, price_per_unit, market_location, phone) VALUES (?, ?, ?, ?, ?, ?)",
                  (user_id, market_name, available_goods, price_per_unit, market_location, phone))
        db.commit()

        flash("Market details submitted successfully!", 'success')

    db.close()
    return render_template('market_dashboard.html', products=products, messages=formatted_messages)


# # API to send message
# @app.route('/send_message', methods=['POST'])
# def send_message():
#     if 'user_id' not in session:
#         return jsonify({'status': 'error', 'message': 'Not logged in'}), 401
    
#     try:
#         data = request.get_json()
#         if not data:
#             return jsonify({'status': 'error', 'message': 'No data received'}), 400
            
#         recipient_id = data.get('recipient_id')
#         message = data.get('message')
        
#         if not recipient_id or not message:
#             return jsonify({'status': 'error', 'message': 'Missing recipient_id or message'}), 400
        
#         db = get_db()
        
#         # Get sender's name
#         user = db.execute("SELECT name FROM users WHERE id = ?", (session['user_id'],)).fetchone()
#         name = user['name']
        
#         db.execute("""
#             INSERT INTO messages (sender_id, recipient_id, message, timestamp, name)
#             VALUES (?, ?, ?, ?, ?)
#         """, (session['user_id'], recipient_id, message, datetime.now(), name))
#         db.commit()
        
#         return jsonify({
#             'status': 'success', 
#             'message': 'Message sent',
#             'sender_id': session['user_id'],
#             'recipient_id': recipient_id,
#             'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#         })
        
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 500
#     finally:
#         db.close()

# # API to get messages
# @app.route('/get_messages', methods=['GET'])
# def get_messages():
#     if 'user_id' not in session:
#         return jsonify({'status': 'error', 'message': 'Not logged in'}), 401
    
#     db = get_db()
#     messages = db.execute("""
#         SELECT m.id, m.sender_id, m.recipient_id, m.message, m.timestamp, m.is_read, u.name as sender_name 
#         FROM messages m
#         JOIN users u ON m.sender_id = u.id
#         WHERE m.recipient_id = ?
#         ORDER BY m.timestamp DESC
#     """, (session['user_id'],)).fetchall()
    
#     # Mark messages as read
#     db.execute("UPDATE messages SET is_read = 1 WHERE recipient_id = ?", (session['user_id'],))
#     db.commit()
#     db.close()
    
#     messages_list = []
#     for msg in messages:
#         messages_list.append({
#             'id': msg['id'],
#             'sender_name': msg['name'],
#             'message': msg['message'],
#             'timestamp': msg['timestamp']
#         })
    
#     return jsonify({'status': 'success', 'messages': messages_list})
from datetime import datetime
from flask import request, jsonify, session
import sqlite3

@app.route('/send_message', methods=['POST'])
def send_message():
    # Debug: Print received data
    print("Received send_message request with data:", request.json)
    
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Not logged in'}), 401
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': 'No data received'}), 400
        
        recipient_id = data.get('recipient_id')
        message = data.get('message')
        
        if not recipient_id or not message:
            return jsonify({'status': 'error', 'message': 'Missing recipient_id or message'}), 400
        
        # Debug: Print before DB operation
        print(f"Preparing to send message from {session['user_id']} to {recipient_id}")
        
        db = get_db()
        
        # Get sender's name from the database
        user_id = session['user_id']
        query = "SELECT name FROM users WHERE id = ?"
        cursor = db.cursor()
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        
        if result:
            name = result[0]
        
            # Insert the new message into the messages table
            cursor.execute("""
                INSERT INTO messages (sender_id, recipient_id, message, timestamp, name)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, recipient_id, message, datetime.now(), name))
            db.commit()
            
            # Debug: Print success
            print("Message successfully saved to database")
            
            return jsonify({
                'status': 'success', 
                'message': 'Message sent',
                'sender_id': user_id,
                'recipient_id': recipient_id,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            })
        else:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404

    except Exception as e:
        # Debug: Print error
        print(f"Error sending message: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        db.close()
@app.route('/get_messages', methods=['GET'])
def get_messages():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Not logged in'}), 401
    
    db = get_db()
    cursor = db.cursor()
    
    # Fetch messages for the logged-in user
    cursor.execute("""
        SELECT m.id, m.sender_id, m.recipient_id, m.message, m.timestamp, m.is_read, u.name as sender_name 
        FROM messages m
        JOIN users u ON m.sender_id = u.id
        WHERE m.recipient_id = ?
        ORDER BY m.timestamp DESC
    """, (session['user_id'],))
    
    messages = cursor.fetchall()
    
    # Mark messages as read
    cursor.execute("UPDATE messages SET is_read = 1 WHERE recipient_id = ?", (session['user_id'],))
    db.commit()
    
    cursor.close()
    
    messages_list = []
    for msg in messages:
        messages_list.append({
            'id': msg[0],
            'sender_name': msg[6],  # Access sender_name correctly from the result
            'message': msg[3],
            'timestamp': msg[4]  # Ensure timestamp format is consistent
        })
    
    db.close()
    
    return jsonify({'status': 'success', 'messages': messages_list})




# buypage

# @app.route('/buy')
# def buy():
#     product_id = request.args.get('product_id')
#     product_name = request.args.get('product_name')
#     price_per_kg = request.args.get('price_per_kg')
#     farmer_name = request.args.get('farmer_name')
#     return render_template('buy.html', product_name=product_name, price_per_kg=price_per_kg, farmer_name=farmer_name)

@app.route('/buy')
def buy():
    product_id = request.args.get('product_id')
    product_name = request.args.get('product_name')
    price_per_kg = request.args.get('price_per_kg')
    farmer_name = request.args.get('farmer_name')
    
    # Get available quantity from database
    db = get_db()
    try:
        farmer = db.execute(
            "SELECT available_kgs FROM farmer WHERE farmer_name = ?", 
            (farmer_name,)
        ).fetchone()
        
        if farmer:
            available_kgs = float(farmer['available_kgs'])
        else:
            available_kgs = 0.0
            flash('Farmer not found in database', 'warning')
    except Exception as e:
        print(f"Error fetching available quantity: {str(e)}")
        available_kgs = 0.0
        flash('Error fetching product availability', 'danger')
    finally:
        db.close()
    
    return render_template('buy.html', 
                         product_id=product_id,
                         product_name=product_name,
                         price_per_kg=price_per_kg,
                         farmer_name=farmer_name,
                         available_kgs=available_kgs)



# ==========================================================


# API to get users for messaging
@app.route('/get_users', methods=['GET'])
def get_users():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Not logged in'}), 401
    
    db = get_db()
    if session['user_role'] == 'farmer':
        users = db.execute("SELECT id, name FROM users WHERE role = 'market'").fetchall()
    else:
        users = db.execute("SELECT id, name FROM users WHERE role = 'farmer'").fetchall()
    db.close()
    
    users_list = [{'id': user['id'], 'name': user['name']} for user in users]
    return jsonify({'status': 'success', 'users': users_list})

# Route for showing buy form
@app.route('/showBuyForm', methods=['POST'])
def showBuyForm():
    if not request.json:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400

    data = request.json
    product_id = data.get('product_id')
    market_name = data.get('market_name')
    quantity_kg = data.get('quantity_kg')
    total_price = data.get('total_price')
    farmer_name = data.get('farmer_name')
    # product_name = data.get('product_name')
    # Save the order to the database
    db = get_db()
    db.execute("""
        INSERT INTO orders (product_id, market_name, quantity_kg, total_price, farmer_name)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (product_id, market_name, quantity_kg, total_price, farmer_name))
    db.commit()
    db.close()
    
    return jsonify({'status': 'success', 'message': 'Order placed successfully!'})

# Route for submitting orders
@app.route('/submit_order', methods=['POST'])
def submit_order():
    product_id = request.form['product_id']
    
    # product_name = request.form['product_name']
    
    market_name = request.form['market_name']
    kg_quantity = int(request.form['kg_quantity'])
    payment_method = request.form['payment_method']
    
    try:
        if payment_method == "cash":
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error"})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error"})

# Route for placing orders
@app.route('/place_order', methods=['POST'])
def place_order():
    try:
        # Get the order data from the request
        data = request.get_json()
        
        # Validate the data to ensure all necessary fields are present
        if not all(key in data for key in ['product_id', 'market_name', 'quantity_kg', 'total_price', 'payment_method', 'farmer_name',]):
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        # Get database connection
        db = get_db()
        
        # Insert the order into the orders table
        db.execute('''
            INSERT INTO orders (product_id,  market_name, quantity_kg, total_price, payment_method, farmer_name )
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['product_id'], 
           
            data['market_name'], 
            data['quantity_kg'], 
            data['total_price'], 
            data['payment_method'], 
            data['farmer_name'],

           
        ))
        
        # Commit the transaction and close the connection
        db.commit()
        db.close()
        
        return jsonify({"status": "success", "message": "Order placed successfully!"})

    except Exception as e:
        print("Error placing order:", e)
        return jsonify({"status": "error", "message": "Error placing order. Please try again."}), 500
# from flask import request, jsonify
# from datetime import datetime
# import time

# @app.route('/place_order', methods=['POST'])
# def place_order():
#     start_time = time.time()  # For performance measurement
    
#     try:
#         data = request.get_json()

#         # Check for required fields
#         required_fields = ['product_id', 'market_name', 'quantity_kg', 'total_price', 'payment_method', 'farmer_name', 'product_name']
#         missing = [field for field in required_fields if field not in data or not data[field]]
#         if missing:
#             return jsonify({
#                 "status": "error", 
#                 "message": f"Missing required fields: {', '.join(missing)}"
#             }), 400

#         # Insert into database
#         db = get_db()
#         db.execute('''
#             INSERT INTO orders (product_id, market_name, quantity_kg, total_price, payment_method, farmer_name, product_name)
#             VALUES (?, ?, ?, ?, ?, ?, ?)
#         ''', (
#             data['product_id'],
#             data['market_name'],
#             data['quantity_kg'],
#             data['total_price'],
#             data['payment_method'],
#             data['farmer_name'],
#             data['product_name']
#         ))
#         db.commit()
#         db.close()

#         duration = time.time() - start_time  # Check how long it took
#         print(f"Order placed in {duration:.3f} seconds")

#         return jsonify({"status": "success", "message": "Order placed successfully!"})

#     except Exception as e:
#         print("❌ Error placing order:", str(e))
#         return jsonify({"status": "error", "message": "Error placing order. Please try again."}), 500
# @app.route('/place_order', methods=['POST'])
# def place_order():
#     start_time = time.time()
#     try:
#         data = request.get_json()
#         print("📥 Received order data:", data)  # ✅ Log incoming data

#         # Required fields
#         required_fields = ['product_id', 'market_name', 'quantity_kg', 'total_price', 'payment_method', 'farmer_name']
#         missing = [field for field in required_fields if not data.get(field)]
#         if missing:
#             return jsonify({
#                 "status": "error",
#                 "message": f"Missing required fields: {', '.join(missing)}"
#             }), 400

#         # Insert into DB
#         db = get_db()
#         db.execute('''
#             INSERT INTO orders (product_id, market_name, quantity_kg, total_price, payment_method, farmer_name, )
#             VALUES (?, ?, ?, ?, ?, ?)
#         ''', (
#             data['product_id'],
#             data['market_name'],
#             data['quantity_kg'],
#             data['total_price'],
#             data['payment_method'],
#             data['farmer_name']
          
#         ))
#         db.commit()
#         db.close()

#         print(f"✅ Order placed successfully in {time.time() - start_time:.2f} seconds")
#         return jsonify({"status": "success", "message": "Order placed successfully!"})

#     except Exception as e:
#         print("❌ Error placing order:", str(e))
#         return jsonify({"status": "error", "message": "Internal server error"}), 500



# # Route for payment success page
# @app.route('/payment_success')
# def payment_success():
#     return render_template('payment_success.html')

@app.route('/order')
def buy_page():
    db = get_db()
    orders = db.execute("SELECT * FROM orders ORDER BY created_at DESC").fetchall()
    db.close()
    return render_template('order.html', orders=orders)


# Logout route
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200


# ----------------
# Replace with your actual DB path
DATABASE = 'registration_dbs.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This allows us to access rows as dictionaries
    return conn

@app.route('/price_history')
def price_history():
    import sqlite3  # or your DB connector

    conn = sqlite3.connect('registration_dbs.db')
    cursor = conn.cursor()

    # Replace 'farmer' with your actual table name
    cursor.execute("SELECT farmer_name, crops_grown, rate_per_kg, available_kgs, location, phone FROM farmer")
    farmer_data = cursor.fetchall()

    conn.close()

    # Pass the data to the HTML page
    return render_template('price_history.html', farmers=farmer_data)

# if __name__ == '__main__':
#     app.run(debug=True)


# def alter_orders_table():
#     with app.app_context():
#         db = get_db()
#         try:
#             db.execute("ALTER TABLE orders ADD COLUMN product_name TEXT")
#             db.commit()
#             print("✅ 'product_name' column added to 'orders' table.")
#         except sqlite3.OperationalError as e:
#             if "duplicate column name" in str(e).lower():
#                 print("ℹ️ 'product_name' column already exists.")
#             else:
#                 print("❌ Error altering 'orders' table:", e)
#         finally:
#             db.close()


if __name__ == '__main__':
    with app.app_context():
        init_db()
        # alter_orders_table() 
    app.run(debug=True)
