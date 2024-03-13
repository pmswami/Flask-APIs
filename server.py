from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)


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
        return redirect(url_for("user", usr=usr))
    else:
        return render_template("login.html")


@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"


if __name__ == "__main__":
    app.run(debug=True)
