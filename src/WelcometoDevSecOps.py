from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
  # Use render_template to render a welcome message
  return render_template("index.html", message="Welcome to DevSecOps CI/CD with Kubernetes - NYIT Project!")

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)

# Create a new template file index.html to display the message
print("""<!DOCTYPE html>
<html>
<body>
  <h1>{{ message }}</h1>
</body>
</html>""")