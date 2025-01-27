from flask import Flask, jsonify, request, render_template_string, make_response, send_from_directory
import sqlite3
import pickle
import os

app = Flask(__name__)

# Example database (vulnerable to SQL injection)
DATABASE = "test.db"

# Initialize the database if it doesn't exist
def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
        cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'password123')")
        conn.commit()
        conn.close()

# Route 1: SQL Injection vulnerability
@app.route("/user/<username>")
def get_user(username):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # Vulnerable query allowing SQL injection
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    if user:
        return jsonify({"user": user})
    else:
        return jsonify({"error": "User not found"}), 404

# Route 2: Cross-Site Scripting (XSS) vulnerability
@app.route("/xss", methods=["GET", "POST"])
def xss():
    if request.method == "POST":
        name = request.form.get("name")
        # Directly render user input (vulnerable to XSS)
        template = f"<h1>Hello, {name}!</h1>"
        return render_template_string(template)
    return '''
        <form method="POST">
            <input type="text" name="name" placeholder="Enter your name" />
            <button type="submit">Submit</button>
        </form>
    '''

# Route 3: Insecure Deserialization vulnerability
@app.route("/deserialize", methods=["GET", "POST"])
def deserialize():
    if request.method == "POST":
        try:
            # Parse the JSON data
            data = request.get_json()
            return jsonify({"message": "Deserialization successful", "data": data})
        except Exception as e:
            return jsonify({"error": "Invalid or unsafe data", "details": str(e)}), 400
    else:
        return jsonify({"message": "Please send a POST request with valid data"})

# Route 4: Sensitive Data Exposure
@app.route("/config")
def config():
    # Exposes sensitive data like environment variables
    return jsonify({"env": dict(os.environ)})

# Route 5: Command Injection vulnerability
@app.route("/ping", methods=["GET"])
def ping():
    target = request.args.get("target", "127.0.0.1")
    # Unsafe use of os.system
    os.system(f"ping -c 1 {target}")
    return jsonify({"message": f"Pinged {target}"})

# Route 6: Directory Traversal vulnerability
@app.route("/read_file", methods=["GET"])
def read_file():
    filename = request.args.get("file", "default.txt")
    # Allows directory traversal
    with open(filename, "r") as file:
        content = file.read()
    return jsonify({"content": content})

# Route 7: Open Redirect vulnerability
@app.route("/redirect")
def open_redirect():
    url = request.args.get("url", "/")
    return f'<a href="{url}">Click here to continue</a>'

# Route 8: Weak Authentication/Hardcoded credentials
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    # Hardcoded credentials
    if username == "admin" and password == "password123":
        response = make_response(jsonify({"message": "Login successful"}))
        # Vulnerable to insecure cookie handling
        response.set_cookie("auth", "true", httponly=False)
        return response
    return jsonify({"error": "Invalid credentials"}), 401

# Route 9: No Rate Limiting
@app.route("/no_rate_limit")
def no_rate_limit():
    return jsonify({"message": "This route has no rate limiting."})

# Route 10: Debug Mode Enabled
@app.route("/")
def home():
    return render_template_string("""
    <h1>Welcome to the Vulnerable Flask Application</h1>
    <p>Explore the vulnerabilities:</p>
    <ul>
        <li><a href="/xss">Cross-Site Scripting (XSS)</a></li>
        <li><a href="/user/admin">SQL Injection</a></li>
        <li><a href="/deserialize" target="_blank">Insecure Deserialization</a></li>
    </ul>
    """)

# Favicon route (to avoid 404)
@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    # Initialize the database
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
