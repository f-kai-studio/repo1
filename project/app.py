import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///tracker.db")

# Configure current date and time for display
now = datetime.datetime.now()


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    userid = session["user_id"]
    now = datetime.datetime.now()

    cash = db.execute("SELECT cash FROM users WHERE id = ?", userid)[0]["cash"]
    shows = db.execute("SELECT * FROM history WHERE user_id = ?", userid)
    balance = 0
    for show in shows:
        total = show["total"]
        if show["type"] == "debit":
            balance += total
        else:
            balance -= total

    return render_template("index.html", cash=cash, shows=shows, usd=usd, balance = balance, now=now)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        return render_template("buy.html", now=now)

    else:
        item = request.form.get("item")
        if not item:
            return apology("Please input valid item")
        quantity = int(request.form.get("quantity"))
        if not quantity or quantity < 1:
            return apology("Invalid quantity")
        category = request.form.get("category")
        if not category:
            return apology("Please input valid category")
        price = float(request.form.get("price"))
        if not price:
            return apology("Invalid price")

        userid = session["user_id"]
        cash = db.execute("SELECT cash FROM users WHERE id = ?", userid)[0]["cash"]

        cost = price * quantity

        db.execute("INSERT INTO history (user_id, name, category, price, quantity, type, total) VALUES (?, ?, ?, ?, ?, 'credit', ?)", userid, item, category, price, quantity, cost)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash - cost, userid)

        return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Validate submission
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username or not password:
            return apology("must input valid username and/or password", 400)
        if confirmation != password:
            return apology("passwords do not match", 400)

        #generate hash of password
        password_hash = generate_password_hash(password)

        # Remember registrant
        try:
            db.execute("INSERT INTO users (username, hash, cash) VALUES(?, ?, 0)", username, password_hash)
        except:
            return apology("Username already exists", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:

        return render_template("register.html")


@app.route("/update", methods=["GET", "POST"])
@login_required
def update():
    if request.method == "GET":
        return render_template("update.html", now=now)

    else:
        userid = session["user_id"]

        item = request.form.get("item")
        if not item:
            return apology("Please input valid item")
        quantity = int(request.form.get("quantity"))
        if not quantity or quantity < 1:
            return apology("Invalid quantity")
        category = request.form.get("category")
        if not category:
            return apology("Please input valid category")

        cash = db.execute("SELECT cash FROM users WHERE id = ?", userid)[0]["cash"]

        update = float(request.form.get("update"))
        if not update or update < 0:
            return apology("Input valid positive amount")
        else:
            cost = update * quantity
            db.execute("INSERT INTO history (user_id, name, category, price, quantity, type, total) VALUES (?, ?, ?, ?, ?, 'debit', ?)", userid, item, category, update, quantity, cost)
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash + cost, userid)

        return redirect("/")


@app.route("/log", methods=["GET", "POST"])
@login_required
def log():
    """Log away old expense sheet"""
    if request.method == "GET":
        return render_template("log.html", now=now)

    else:
        monthyear = request.form.get("monthyear")

        if not monthyear:
            return apology("input valid month and year")
        else:
            rows = db.execute("SELECT * FROM history WHERE user_id = ?", session["user_id"])
            for row in rows:
                db.execute("INSERT INTO log (user_id, name, category, price, quantity, type, total, monthyear) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", session["user_id"], row["name"], row["category"], row["price"], row["quantity"], row["type"], row["total"], monthyear)

        return redirect("/")


@app.route("/logged")
@login_required
def logged():
    shows = db.execute("SELECT * FROM log WHERE user_id = ?", session["user_id"])
    balance = 0
    for show in shows:
        total = show["total"]
        if show["type"] == "debit":
            balance += total
        else:
            balance -= total

    return render_template("logged.html", usd=usd, shows=shows, now=now, balance=balance)


@app.route("/refresh", methods=["GET", "POST"])
@login_required
def refresh():
    if request.method == "GET":
        return render_template("refresh.html", now=now)
    else:
        db.execute("DELETE FROM history WHERE user_id = ?", session["user_id"])

        return redirect("/")