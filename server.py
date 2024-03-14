from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(minutes=5)
app.secret_key = "Hello world"


@app.route("/")
def home():
    return "Hello World!"


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
        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


# @app.route("/<usr>")
# def user(usr):
#     return f"<h1>{usr}</h1>"


@app.route("/user")
def user():
    if "user" in session:
        usr = session["user"]
        return f"<h1>{usr}</h1>"
    else:
        return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
