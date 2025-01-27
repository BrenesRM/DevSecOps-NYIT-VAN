from flask import Flask, jsonify, request, render_template_string, make_response, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import sqlite3
import os
import re

app = Flask(__name__)

# Secure configurations
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "supersecretkey")  # Secure default secret key
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_HTTPONLY"] = True

# Rate limiting setup
limiter = Limiter(get_remote_address, app=app, default_limits=["10 per minute"])

DATABASE = "test.db"

# Initialize the database securely
def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
        # Store hashed passwords
        hashed_password = generate_password_hash("password123")
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", hashed_password))
        conn.commit()
        conn.close()

# Secure route: SQL Injection mitigation using parameterized queries
@app.route("/user/<username>")
def get_user(username):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return jsonify({"user": {"id": user[0], "username": user[1]}})
    else:
        return jsonify({"error": "User not found"}), 404

# Secure route: XSS mitigation by escaping user input
@app.route("/xss", methods=["GET", "POST"])
def xss():
    if request.method == "POST":
        name = request.form.get("name", "").replace("<", "&lt;").replace(">", "&gt;")
        template = f"<h1>Hello, {name}!</h1>"
        return render_template_string(template)
    return '''
        <form method="POST">
            <input type="text" name="name" placeholder="Enter your name" />
            <button type="submit">Submit</button>
        </form>
    '''

@app.route("/deserialize", methods=["GET", "POST"])
def deserialize():
    if request.method == "POST":
        try:
            # Parse the JSON data
            data = request.get_json()
            return jsonify({"message": "Deserialization successful", "data": data})
        except Exception as e:
            return jsonify({"error": "Invalid or unsafe data", "details": str(e)}), 400
    else:  # Handle GET requests
        return jsonify({"message": "Please send a POST request with valid JSON data."})

# Remove sensitive data exposure
@app.route("/config")
def config():
    return jsonify({"error": "Access denied"}), 403

# Secure route: Prevent command injection
@app.route("/ping", methods=["GET"])
@limiter.limit("5 per minute")
def ping():
    target = request.args.get("target", "127.0.0.1")
    # Validate input to prevent command injection
    if not re.match(r"^[a-zA-Z0-9.\-]+$", target):
        return jsonify({"error": "Invalid target"}), 400
    response = os.system(f"ping -c 1 {target}")
    if response == 0:
        return jsonify({"message": f"Pinged {target}"})
    else:
        return jsonify({"error": f"Unable to ping {target}"}), 500

# Secure route: Prevent directory traversal
@app.route("/read_file", methods=["GET"])
def read_file():
    filename = request.args.get("file", "default.txt")
    safe_filename = os.path.basename(filename)  # Prevent directory traversal
    try:
        with open(safe_filename, "r") as file:
            content = file.read()
        return jsonify({"content": content})
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

# Secure route: Prevent open redirects
@app.route("/redirect")
def open_redirect():
    url = request.args.get("url", "/")
    if not url.startswith("/"):
        return jsonify({"error": "Invalid redirect URL"}), 400
    return f'<a href="{url}">Click here to continue</a>'

# Secure route: Strong authentication
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    query = "SELECT password FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    conn.close()
    if user and check_password_hash(user[0], password):
        response = make_response(jsonify({"message": "Login successful"}))
        response.set_cookie("auth", "true", httponly=True, secure=True)
        return response
    return jsonify({"error": "Invalid credentials"}), 401

# Rate limiting for all users
@app.route("/no_rate_limit")
@limiter.limit("10 per hour")
def no_rate_limit():
    return jsonify({"message": "This route is now rate-limited."})

# Disable debug mode for production
@app.route("/")
def home():
    return render_template_string("""
    <h1>Welcome to the Secure Flask Application</h1>
    <p>Explore the secure routes:</p>
    <ul>
        <li><a href="/xss">Cross-Site Scripting (XSS)</a></li>
        <li><a href="/user/admin">SQL Injection</a></li>
        <li><a href="/deserialize">Insecure Deserialization</a></li>
    </ul>
    """)

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
