from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import bcrypt
from flask import jsonify
from datetime import datetime
import random  # Import the random module

app = Flask(__name__)


# Configure MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'registration_dbs'
mysql = MySQL(app)
# Secret Key for Flash Messages and Sessions
app.secret_key = 'your_secret_key'

# Global variable for alerts
farmer_alerts = []
market_alerts = []

# Route for Login Page
@app.route('/')
def index():
    return render_template('home.html')
@app.route('/gov_schems')
def gov_schems():
    return render_template('gov_schems.html')  # You'll need to create this page
# @app.route('/')
# def index():
#     return render_template('login.html')
# @app.route('/chat')
# def chat():
#     return render_template('chat.html')
########################################
from flask import Flask, render_template, request, jsonify
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


######################################################


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

        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO users (name, location, phone, password, role) VALUES (%s, %s, %s, %s, %s)", 
                        (name, location, phone, hashed_password, role))
            mysql.connection.commit()
            cur.close()
            flash("You have successfully registered! Please log in.", 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f"An error occurred: {str(e)}", 'danger') 
            return redirect(url_for('register'))
    return render_template('register.html')

# Route for Login Page
# -------------------------------------------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE phone = %s", (phone,))
        user = cur.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[4].encode('utf-8')):
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            session['user_role'] = user[5]
            flash("Login successful!", 'success')

            if user[5] == 'farmer':
                return redirect(url_for('farmer_dashboard'))
            else:
                return redirect(url_for('market_dashboard'))
        else:
            flash("Incorrect phone number or password.", 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

# Route for Farmer Dashboard
# -------------------------------------------------------------------------------------------------------
# @app.route('/farmer_dashboard', methods=['GET', 'POST'])
# def farmer_dashboard():
#     if 'user_id' not in session:
#         flash("You must log in first!", 'danger')
#         return redirect(url_for('login'))

#     if request.method == 'POST':
#         user_id = session['user_id']
#         farmer_name = request.form['farmer_name']
#         crops_grown = request.form['crops_grown']
#         rate_per_kg = request.form['rate_per_kg']
#         available_kgs = request.form['available_kgs']
#         location = request.form['location']
        
#         cur = mysql.connection.cursor()
#         cur.execute("INSERT INTO farmer (user_id, farmer_name, crops_grown, rate_per_kg, available_kgs, location) VALUES (%s, %s, %s, %s, %s, %s)",
#                   (user_id, farmer_name, crops_grown, rate_per_kg, available_kgs, location))
#         mysql.connection.commit()
#         cur.close()
#         flash("Farmer details submitted successfully!", 'success')

#     # Check for new messages
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM messages WHERE recipient_id = %s AND is_read = 0", (session['user_id'],))
#     new_messages = cur.fetchall()
#     cur.close()

#     return render_template('farmer_dashboard.html', messages=new_messages)

import random  

@app.route('/farmer_dashboard', methods=['GET', 'POST'])
def farmer_dashboard():
    if 'user_id' not in session:
        flash("You must log in first!", 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        user_id = session['user_id']
        farmer_name = request.form['farmer_name']
        crops_grown = request.form['crops_grown']
        available_kgs = int(request.form['available_kgs'])  # Convert to integer
        location = request.form['location']
        phone =request.form['phone']

        # Assign 
        if available_kgs == 1:
            rate_per_kg = round(random.uniform(25, 100), 2)  
        elif available_kgs > 1000:
            rate_per_kg = round(random.uniform(500, 200), 2)  
        else:
            rate_per_kg = round(random.uniform(100, 200), 2)  
        
            
        # Insert into the database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO farmer (user_id, farmer_name, crops_grown, rate_per_kg, available_kgs, location, phone) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                  (user_id, farmer_name, crops_grown, rate_per_kg, available_kgs, location, phone))
        mysql.connection.commit()
        cur.close()
        flash("Farmer details submitted successfully!", 'success')

    # Check for new messages
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM messages WHERE recipient_id = %s AND is_read = 0", (session['user_id'],))
    new_messages = cur.fetchall()
    cur.close()

    return render_template('farmer_dashboard.html', messages=new_messages)


# Route for Market Dashboard
# -------------------------------------------------------------------------------------------------------
@app.route('/market_dashboard', methods=['GET', 'POST'])
def market_dashboard():
    if 'user_id' not in session:
        flash("You must log in first!", 'danger')
        return redirect(url_for('login'))

    # Fetch all products
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM farmer")
    products = cur.fetchall()
    
    # Check for new messages
    cur.execute("SELECT * FROM messages WHERE recipient_id = %s AND is_read = 0", (session['user_id'],))
    new_messages = cur.fetchall()
    cur.close()
    
    if request.method == 'POST':
        user_id = session['user_id']
        market_name = request.form['market_name']
        available_goods = request.form['available_goods']
        price_per_unit = request.form['price_per_unit']
        market_location = request.form['market_location']
        phone =request.form['phone']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO market (user_id, market_name, available_goods, price_per_unit, market_location, phone) VALUES (%s, %s, %s, %s, %s, %s)",
                  (user_id, market_name, available_goods, price_per_unit, market_location, phone))
        mysql.connection.commit()
        cur.close()
        flash("Market details submitted successfully!", 'success')

    return render_template('market_dashboard.html', products=products, messages=new_messages)

# API to send message
# -------------------------------------------------------------------------------------------------------
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
        
        
             
             

        cur = mysql.connection.cursor()
        
        
        
        user_id = session['user_id']

# Execute the query using parameterized input
        query = "SELECT name FROM users WHERE id = %s"
        cur.execute(query, (user_id,))

# Fetch result
        result = cur.fetchone()
        
        name = result[0]
        
        cur.execute("""
            INSERT INTO messages (sender_id, recipient_id, message, timestamp , name)
            VALUES (%s, %s, %s, %s, %s)
        """, (session['user_id'], recipient_id, message, datetime.now() , name))
        mysql.connection.commit()
        
        # Debug: Print success
        print("Message successfully saved to database")
        
        return jsonify({
            'status': 'success', 
            'message': 'Message sent',
            'sender_id': session['user_id'],
            'recipient_id': recipient_id,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            
        })
        
    except Exception as e:
        # Debug: Print error
        print(f"Error sending message: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        cur.close()

# API to get messages
# -------------------------------------------------------------------------------------------------------
import MySQLdb.cursors

@app.route('/get_messages', methods=['GET'])
def get_messages():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Not logged in'}), 401
    
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  # Use DictCursor to fetch data in dictionary format
    cur.execute("""
        SELECT m.id, m.sender_id, m.recipient_id, m.message, m.timestamp, m.is_read, u.name as sender_name 
        FROM messages m
        JOIN users u ON m.sender_id = u.id
        WHERE m.recipient_id = %s
        ORDER BY m.timestamp DESC
    """, (session['user_id'],))
    
    messages = cur.fetchall()
    
    # Mark messages as read
    cur.execute("UPDATE messages SET is_read = 1 WHERE recipient_id = %s", (session['user_id'],))
    mysql.connection.commit()
    cur.close()
    
    messages_list = []
    for msg in messages:
        messages_list.append({
            'id': msg['id'],
            'sender_name': msg['name'],  # Access sender_name correctly from the result
            'message': msg['message'],
            'timestamp': msg['timestamp'].strftime('%Y-%m-%d %H:%M:%S')  # Ensure timestamp format is consistent
        })
    
    return jsonify({'status': 'success', 'messages': messages_list})

# -------------------------------------------------------------------------------------------------------
# API to get users for messaging
@app.route('/get_users', methods=['GET'])
def get_users():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Not logged in'}), 401
    
    cur = mysql.connection.cursor()
    if session['user_role'] == 'farmer':
        cur.execute("SELECT id, name FROM users WHERE role = 'market'")
    else:
        cur.execute("SELECT id, name FROM users WHERE role = 'farmer'")
    users = cur.fetchall()
    cur.close()
    
    users_list = [{'id': user[0], 'name': user[1]} for user in users]
    return jsonify({'status': 'success', 'users': users_list})


# -------------------------------------------------------------------------------------------------------
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

    # Save the order to the database (you can modify this according to your database schema)
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO orders (product_id, market_name, quantity_kg, total_price, farmer_name)
        VALUES (%s, %s, %s, %s, %s)
    """, (product_id, market_name, quantity_kg, total_price, farmer_name))
    mysql.connection.commit()

    cur.close()
    return jsonify({'status': 'success', 'message': 'Order placed successfully!'})
# -------------------------------------------------------------------------------------------------------

@app.route('/submit_order', methods=['POST'])
def submit_order():
    # Get data from the request
    product_id = request.form['product_id']
    market_name = request.form['market_name']
    kg_quantity = int(request.form['kg_quantity'])
    payment_method = request.form['payment_method']

    # Logic to process the order (e.g., save to database, etc.)
    try:
        # Simulate saving order to the database or further processing
        if payment_method == "cash":
            # Process order (in a real app, you'd save it to the DB)
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error"})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error"})

# -------------------------------------------------------------------------------------------------------
# @app.route('/place_order', methods=['POST'])
# def place_order():
#     data = request.get_json()
#     # Process the order (e.g., save to database, etc.)
#     # In this case, we're just logging the order for demonstration
#     product_id = data.get('product_id')
#     market_name = data.get('market_name')
#     quantity_kg = data.get('quantity_kg')
#     total_price = data.get('total_price')
#     farmer_name = data.get('farmer_name')
    
#     # You would usually store the order in a database here
#     print(f"Order placed: {product_id}, {market_name}, {quantity_kg}kg, ₹{total_price}, Farmer: {farmer_name}")

#     # Simulate a successful order placement
#     return jsonify({'status': 'success'})
from flask import Flask, request, jsonify, render_template
import sqlite3


# Function to create the orders table in SQLite if it doesn't exist
def create_orders_table():
    conn = sqlite3.connect('market.db')  # Replace 'market.db' with your database file path
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            market_name TEXT,
            quantity INTEGER,
            total_price REAL,
            payment_method TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Call the function to create the table when the app starts
create_orders_table()

@app.route('/place_order', methods=['POST'])
def place_order():
    try:
        # Extract form data from the request
        data = request.get_json()
        print("Received data:", data)  # Log incoming data for debugging
        
        # Validate the data
        required_fields = ['market_name', 'quantity_kg', 'total_price', 'payment_method']
        if not all(field in data for field in required_fields):
            return jsonify({"status": "error", "message": "Missing required fields!"}), 400
        
        # Extract values from the incoming data
        market_name = data['market_name']
        quantity = data['quantity_kg']
        total_price = data['total_price']
        payment_method = data['payment_method']
        
        # Insert data into the orders table
        conn = sqlite3.connect('market.db')  # Ensure this path is correct
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO orders ( market_name, quantity, total_price, payment_method)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ( market_name, quantity, total_price, payment_method))
        
        # Commit and close the connection
        conn.commit()
        conn.close()
        
        return jsonify({"status": "success", "message": "Order placed successfully!"})

    except Exception as e:
        print("Error placing order:", e)  # Log any errors
        return jsonify({"status": "error", "message": "Error placing order. Please try again."}), 500

# Route to render a success page (optional)
@app.route('/payment_success')
def payment_success():
    return render_template('payment_success.html')  # Adjust according to your needs


# ---------------------------------------------------------------------------
# @app.route('/place_order', methods=['POST'])
# def place_order():
#     data = request.get_json()
#     product_id = data.get('product_id')
#     market_name = data.get('market_name')
#     quantity_kg = data.get('quantity_kg')
#     total_price = data.get('total_price')
#     farmer_name = data.get('farmer_name')

#     cur = mysql.connection.cursor()

#     # 🔍 Get farmer_id using product_id from 'farmer' table
#     cur.execute("SELECT user_id FROM farmer WHERE id = %s", (product_id,))
#     farmer = cur.fetchone()

#     if not farmer:
#         return jsonify({'status': 'error', 'message': 'Farmer not found'}), 404

#     farmer_id = farmer[0]

#     # 📝 Insert order into DB
#     cur.execute("""
#         INSERT INTO orders (product_id, market_name, quantity_kg, total_price, farmer_name, farmer_id)
#         VALUES (%s, %s, %s, %s, %s, %s)
#     """, (product_id, market_name, quantity_kg, total_price, farmer_name, farmer_id))

#     mysql.connection.commit()
#     cur.close()

#     return jsonify({'status': 'success'})
# @app.route('/view_orders')
# def view_orders():
#     if 'user_id' not in session:
#         flash("You must log in first!", 'danger')
#         return redirect(url_for('login'))

#     # Only farmers should access this page
#     if session['user_role'] != 'farmer':
#         flash("Access denied!", 'danger')
#         return redirect(url_for('login'))

#     cur = mysql.connection.cursor()
#     cur.execute("""
#         SELECT o.id, f.crops_grown, o.market_name, o.quantity_kg, o.total_price, o.farmer_name
#         FROM orders o
#         JOIN farmer f ON o.product_id = f.id
#         WHERE o.farmer_id = %s
#         ORDER BY o.id DESC
#     """, (session['user_id'],))

#     orders = cur.fetchall()
#     cur.close()

#     return render_template('view_orders.html', orders=orders)
# ----------------------------------
db_config = {
    'host': 'localhost',
    'user': 'root',      # Default XAMPP username
    'password': '',      # Default XAMPP password (empty)
    'database': 'registration_dbs'
}

# @app.route('/place_order', methods=['POST'])
# def place_order():
#     try:
#         data = request.get_json()
        
#         # Connect to MySQL database
#         conn = mysql.connector.connect(**db_config)
#         cursor = conn.cursor()
        
#         # Insert order into database
#         query = """
#         INSERT INTO orders 
#         (product_id, market_name, quantity_kg, total_price, farmer_name, payment_method) 
#         VALUES (%s, %s, %s, %s, %s, %s)
#         """
#         values = (
#             data['product_id'],
#             data['market_name'],
#             data['quantity_kg'],
#             data['total_price'],
#             data['farmer_name'],
#             data['payment_method']
#         )
        
#         cursor.execute(query, values)
#         conn.commit()
        
#         cursor.close()
#         conn.close()
        
#         return jsonify({
#             'status': 'success',
#             'message': 'Order placed successfully'
#         })
        
#     except Exception as e:
#         return jsonify({
#             'status': 'error',
#             'message': str(e)
#         }), 500


# # -----------------------------------------------------------------------------------------------------------
# # Payment success page route
# @app.route('/payment_success')
# def payment_success():
#     return render_template('payment_success.html')
# -------------------------------------------------------------------------------------------------------

# Logout route
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200
# -------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)