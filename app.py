from flask import Flask, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            raw_password TEXT NOT NULL,
            hashed_password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def insert_user(email, raw_password, hashed_password):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (email, raw_password, hashed_password) VALUES (?, ?, ?)",
                   (email, raw_password, hashed_password))
    conn.commit()
    conn.close()

def get_user(email):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user

# 🔹 Тіркелу
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        raw_password = request.form["raw_password"]
        hashed_password = request.form["hashed_password"]

        if get_user(email):
            return "❌ Бұл email тіркелген! <a href='/login'>Кіру</a>"

        insert_user(email, raw_password, hashed_password)
        return "✅ Сәтті тіркелдіңіз! <a href='/login'>Кіру</a>"

    return '''
    <h2>Тіркелу</h2>
    <form method="POST">
        Email: <input type="email" name="email" required><br><br>
        Құпия сөз: <input type="password" id="raw" required><br><br>
        <input type="hidden" name="raw_password" id="raw_password">
        <input type="hidden" name="hashed_password" id="hashed_password">
        <button type="submit">Тіркелу</button>
    </form>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/js-sha256/0.9.0/sha256.min.js"></script>
    <script>
      const form = document.querySelector('form');
      form.addEventListener('submit', function(e) {
        const raw = document.getElementById("raw").value;
        document.getElementById("raw_password").value = raw;
        document.getElementById("hashed_password").value = sha256(raw);
      });
    </script>
    '''

# 🔹 Кіру
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        hashed_password = request.form["hashed_password"]

        user = get_user(email)
        if not user:
            return "❌ Қолданушы табылмады! <a href='/register'>Тіркелу</a>"
        if user[3] != hashed_password:
            return "❌ Құпия сөз қате!"
        return f"✅ Қош келдіңіз, {email}!"

    return '''
    <h2>Кіру</h2>
    <form method="POST">
        Email: <input type="email" name="email" required><br><br>
        Құпия сөз: <input type="password" id="login_raw" required><br><br>
        <input type="hidden" name="hashed_password" id="login_hashed">
        <button type="submit">Кіру</button>
    </form>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/js-sha256/0.9.0/sha256.min.js"></script>
    <script>
      const form = document.querySelector('form');
      form.addEventListener('submit', function(e) {
        const raw = document.getElementById("login_raw").value;
        document.getElementById("login_hashed").value = sha256(raw);
      });
    </script>
    '''

@app.route("/")
def index():
    return "<h3>🔐 <a href='/login'>Кіру</a> | <a href='/register'>Тіркелу</a></h3>"

# 🟢 Қосымша импортталғанда да база құрылсын
init_db()
