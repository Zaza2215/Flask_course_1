from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/user/<string:name>/<int:id_user>")
def user(name, id_user):
    return f"About page: {name}<br>ID: {id_user}"


if __name__ == "__main__":
    app.run(debug=True)
