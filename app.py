from flask import Flask, redirect, render_template, request, url_for, session
from flask_mysqldb import MySQL
import hashlib

app = Flask(__name__)
app.jinja_env.filters["zip"] = zip
app.secret_key = "MySecret123Keys"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "catalogbook"

mysql = MySQL(app)
global username

@app.route("/login", methods=["GET", "POST"])
def login():
    if 'loggedin' in session:
        return redirect(url_for("list"))
    else:
        if request.method == "POST" and "username" in request.form and "password" in request.form:
    
            username = request.form["username"]
            password = request.form["password"]
            key = "080"
            key_password = password + key
            h = hashlib.md5(key_password.encode())
            db_password = h.hexdigest()

            print(username, password)

            myCursor = mysql.connection.cursor()
            myCursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, db_password))

            account = myCursor.fetchone()
            if account:
                session["loggedin"] = True
                session["id"] = account[0]
                session["username"] = account[1]
                print(session["username"])
                return redirect(url_for("list"))
            else:
                return render_template("login.html", msg="Username/Password Salah")
    
    return render_template("login.html")
        

@app.route("/logout")
def logout():
    session.pop('loggedin')
    session.pop('id')
    session.pop('username')
    return redirect(url_for("login"))

@app.route("/signup", methods=["POST", "GET"])
def signup():
    msg = ''
    if 'loggedin' in session:
        return redirect(url_for("list"))
    else:
        if request.method == "POST" and "username" in request.form and "password" in request.form:
            username = request.form["username"]
            password = request.form["password"]
            key = "080"
            key_password = password + key
            h = hashlib.md5(key_password.encode())
            db_password = h.hexdigest()
            
            myCursor = mysql.connection.cursor()
            myCursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            account = myCursor.fetchone()

            if account:
                msg = 'Username telah digunakan'
            elif not username or not password:
                msg = 'Isi Username dan Password'
            else:
                myCursor.execute("INSERT INTO users(username, password) VALUES (%s,%s)", (username, db_password))
                mysql.connection.commit()
                return redirect(url_for("login"))

    return render_template("signup.html", msg=msg)

@app.route("/")
def list():
    myCursor = mysql.connection.cursor()
    myCursor.execute("SELECT * From list")
    results = myCursor.fetchall()
    data = []
    for i in results:
        data.append(i)
    if 'loggedin' in session:
        return render_template("tabel.html", data=data, username=session["username"])
    else:
        username = "GUEST"
        return render_template("tabel2.html", data=data, username=username)

@app.route("/tambah", methods=["GET", "POST"])
def tambah():
    if 'loggedin' in session:
        if request.method == "POST":
            details = request.form

            nama = details["nama"]
            penulis = details["penulis"]
            deskripsi = details["deskripsi"]

            myCursor = mysql.connection.cursor()
            myCursor.execute("INSERT INTO list(nama, penulis, deskripsi) VALUES (%s, %s, %s)", (nama, penulis, deskripsi))
            mysql.connection.commit()
            myCursor.close()
            return redirect(url_for("list"))

        return render_template("insert.html")
    else:
        return redirect(url_for("login"))

@app.route("/edit/<id>", methods=["POST", "GET"])
def edit(id):
    if 'loggedin' in session:
        myCursor = mysql.connection.cursor()
        myCursor.execute("SELECT * FROM list WHERE id = %s", (id))
        data = myCursor.fetchone()
        if request.method == "POST":
            details = request.form
            id = details["id"]
            nama = details["nama"]
            penulis = details["penulis"]
            deskripsi = details["deskripsi"]

            myCursor = mysql.connection.cursor()
            myCursor.execute("UPDATE list SET nama=%s, penulis=%s, deskripsi=%s WHERE id=%s", (nama, penulis, deskripsi, id))
            mysql.connection.commit()
            myCursor.close()
            return redirect(url_for("list"))

        return render_template("edit.html", data=data)
    else:
        return redirect(url_for("login"))

@app.route("/hapus/<id>", methods=["POST", "GET"])
def hapus(id):
    if 'loggedin' in session:
        myCursor = mysql.connection.cursor()
        myCursor.execute("DELETE FROM list WHERE id = %s", (id,))
        mysql.connection.commit()
        myCursor.close()
        return redirect(url_for("list"))
    else:
        return redirect(url_for("login"))
app.run(debug=True)