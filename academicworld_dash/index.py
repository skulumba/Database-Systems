from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = '1f4a9f65a0800030c3c3094ab039d1e3'

# Print current working directory to console
print(os.getcwd())

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your pass",
    database="academicworld"
)



@app.route("/")
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = db.cursor()
        try:
            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            user = cursor.fetchone()
            if user:
                return render_template('register.html', error="Username already exists.")
            else:
                cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
                db.commit()
                session['username'] = username
                return redirect("/login")
        except mysql.connector.Error as err:
            return render_template('register.html', error=f"Error: {err}")
    else:
        return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = db.cursor()
        try:
            cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
            user = cursor.fetchone()
            if user:
                session['username'] = user[1]
                return redirect('/dashboard')
            else:
                return render_template('login.html', error="Invalid username or password.")
        except mysql.connector.Error as err:
            return render_template('login.html', error=f"Error: {err}")
    else:
        return render_template('login.html')
    
@app.route("/dashboard")
def dashboard():
    if 'username' in session:
        return redirect('http://127.0.0.1:8050/')
    else:
        return redirect(url_for('login'))

#@app.route("/logout")
#def logout():
 #   session.pop('username', None)
 #   return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()
    print(os.getcwd())
