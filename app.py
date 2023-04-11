from flask import Flask, render_template, jsonify, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from database import load_jobs_from_db, application_to_db
import secrets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///signup.db'
db = SQLAlchemy(app)
app.secret_key = secrets.token_hex(16)


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(50), unique=True, nullable=False)
  email = db.Column(db.String(100), unique=True, nullable=False)
  password = db.Column(db.String(100), nullable=False)


@app.route("/")
def hello_world():
  jobs = load_jobs_from_db()
  return render_template('index.html', jobs=jobs)


@app.route("/Admin", methods=["GET", "POST"])
def admin():
  if request.method == "POST" and request.form.get(
      "emaill") == "Quick123" and request.form.get("passwordd") == "123456789":
    return redirect(url_for("AdminHome"))
  elif request.method == "POST":
    flash("password or email is incorrect", category="error")

  return render_template('Admin.html')


# ------------------------------SIGNUP----------------------------------------------------


@app.route("/signup", methods=["GET", "POST"])
def signupp():
  if request.method == "POST":
    email = request.form.get("email")
    firstName = request.form.get("firstName")
    password1 = request.form.get("password1")
    password2 = request.form.get("password2")
    if len(email) < 4:
      flash("Email must be greater than 4 characters.", category="error")
    elif len(firstName) < 2:
      flash("Name must be greater than 2 characters.", category="error")
    elif password1 != password2:
      flash("Passwords must match.", category="error")
    elif len(password1) < 7:
      flash("Password must be greater than 6 characters.", category="error")
    else:
      # create a new user object
      new_user = User(username=firstName, email=email, password=password1)
      # add the user to the database
      db.session.add(new_user)
      db.session.commit()
      flash("Account created successfully!", category="success")
  return render_template("registration.html")

  #add data to database


# --------------------LOGIN--------------------------------------------------------------------

with app.app_context():

  @app.route("/", methods=["GET", "POST"])
  def login():
    if request.method == "POST":
      email = request.form.get("email")
      password = request.form.get("password")
      user = User.query.filter_by(email=email).first()
      if user:
        if user.password == password:
          flash("Logged in successfully!", category="success")
          # redirect to a logged in page
          return redirect(url_for("Service"))
        else:
          flash("Incorrect password. Please try again.", category="error")
      else:
        flash("User does not exist. Please register first.", category="error")
    return render_template("index.html")


# with app.app_context():
#   users = User.query.all()
#   for user in users:
#     print(user.id, user.username, user.email, user.password)
# 1 Ankit Singh Ankitmsingh2@gmail.com 123456789

# -----------------------------------------------------------------------------------------


@app.route("/forget")
def forget():
  return render_template('forget.html')


# ---------------------------------------------------------------------------------------------
@app.route("/Service")
def Service():
  jobs = load_jobs_from_db()
  return render_template('Service.html', jobs=jobs)


# ---------------------------------------------------------
@app.route("/AdminHome")
def AdminHome():
  return render_template('AdminHome.html')


# -------------------------------------------------------------------------------------------
@app.route("/aboutus")
def Aboutus():
  return render_template('aboutus.html')


# ------------------------------------------------------------------------
@app.route("/AdminHome", methods=["GET", "POST"])
def apply_to_job():
  if request.method == "POST":
    data = request.form
    application_to_db(data)
    flash("details Added successfully!", category="success")
  return render_template("AdminHome.html")


# ================================================================
if __name__ == "__main__":
  with app.app_context():
    db.create_all()
  app.run(host="0.0.0.0", debug=True)
