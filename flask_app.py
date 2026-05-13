from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

USERS_FILE = "users.json"

@app.route("/")
def landing():
    return render_template("land.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        users = load_users()
        if email not in users or users[email]["password"] != password:
            return "Invalid credentials!", 400

        session["logged_in"] = True
        session["email"] = email
        session["name"] = users[email]["name"]
        session["childName"] = users[email].get("childName", "")

        return redirect(url_for("chat"))

    return render_template("login.html")



# ---------------- LOAD USERS ----------------
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    return {u["email"]: u for u in data}
                elif isinstance(data, dict):
                    return data
                else:
                    return {}
            except json.JSONDecodeError:
                return {}
    return {}

# ---------------- SAVE USERS ----------------
def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        users = load_users()
        if email not in users or users[email]["password"] != password:
            return "Invalid credentials!", 400

        # Login successful
        session["logged_in"] = True
        session["email"] = email
        session["name"] = users[email]["name"]
        session["childName"] = users[email].get("childName", "")

        return redirect(url_for("chat"))

    return render_template("login.html")

# ---------------- CREATE ACCOUNT ----------------
@app.route("/create_account", methods=["POST"])
def create_account():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    childName = request.form.get("childName", "")

    if not name or not email or not password:
        return "All fields required!", 400

    users = load_users()
    if email in users:
        return "Email already exists!", 400

    users[email] = {
        "name": name,
        "password": password,
        "childName": childName,
        "stars": 0
    }
    save_users(users)

    # Direct login after create
    session["logged_in"] = True
    session["email"] = email
    session["name"] = name
    session["childName"] = childName

    return redirect(url_for("chat"))

# ---------------- CHAT ----------------
@app.route("/chat")
def chat():
    if not session.get("logged_in"):
        flash("Please login first.", "danger")
        return redirect(url_for("index"))

    users = load_users()
    email = session.get("email")
    user = users.get(email)

    if not user:
        session.clear()
        flash("User not found!", "danger")
        return redirect(url_for("index"))

    return render_template(
        "index.html",
        logged_in=True,
        name=user["name"],
        childName=user.get("childName", ""),
        stars=user.get("stars", 0),
        email=email
    )

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("index"))

# ---------------- ADMIN PANEL ----------------
@app.route("/admin", methods=["GET", "POST"])
def admin():
    ADMIN_EMAIL = "admin@gmail.com"
    ADMIN_PASSWORD = "admin123"

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            users = load_users()
            # Convert dict to list with email included
            users_list = []
            for e, u in users.items():
                u_copy = u.copy()
                u_copy['email'] = e
                users_list.append(u_copy)
            return render_template("admin.html", users=users_list)
        else:
            return "❌ Invalid Admin Credentials", 403
    return render_template("admin.html", users=None)

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)
