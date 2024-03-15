from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Hello world"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)

app.app_context().push()


class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email


@app.route("/")
def home():
    return "Hello World!"


@app.route("/view")
def view():
    return render_template("view.html", values=users.query.all())


# @app.route("/<name>")
# def user(name):
#     return f"Hello {name}"


# @app.route("/admin")
# def admin():
#     # return redirect(url_for("home")) # redirection
#     return redirect(
#         url_for("user", name="Swamfiresss")
#     )  # for redirection with arguments


# @app.route("/templates/")
# def templates():
#     # return render_template("index.html", content = "Swamfire")
#     return render_template("index.html", content=[1, 2, 3])


# @app.route("/test/")
# def test():
#     # return render_template("index.html", content = "Swamfire")
#     return render_template("index1.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        usr = request.form["nm"]
        session.permanent = True
        session["user"] = usr
        # return redirect(url_for("user", usr=usr))
        found_user = users.query.filter_by(name=usr).first()
        if found_user:
            session["email"] = found_user.email
        else:
            usr_data = users(usr, "")
            db.session.add(usr_data)
            db.session.commit()

        flash("Login Successful!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already Logged In !")
            return redirect(url_for("user"))
        return render_template("login.html")


@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        # flash(f"You have been logged out {user}", "info")
    session.pop("user", None)
    session.pop("email", None)
    flash("You have been logged out", "info")
    return redirect(url_for("login"))


# @app.route("/<usr>")
# def user(usr):
#     return f"<h1>{usr}</h1>"


@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        usr = session["user"]
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=usr).first()
            found_user.email = email
            db.session.commit()
            flash("Your email was saved!", "info")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html", user=usr, email=email)  # f"<h1>{usr}</h1>"
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))


if __name__ == "__main__":

    # creates tables in database
    db.create_all()

    app.run(debug=True)
