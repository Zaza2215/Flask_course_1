from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///blog.db'
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Article {self.id}>"


@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/create-article", methods=["POST", "GET"])
def create_article():
    if request.method == "POST":
        title = request.form["title"]
        intro = request.form["intro"]
        text = request.form["text"]

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect("/posts")
        except Exception as ex:
            print(ex)
            return "An error occurred while adding!"
    else:
        return render_template("create_article.html")


@app.route("/posts/<int:id_post>/update", methods=["POST", "GET"])
def update_article(id_post):
    article = Article.query.get(id_post)
    if request.method == "POST":
        article.title = request.form["title"]
        article.intro = request.form["intro"]
        article.text = request.form["text"]

        try:
            db.session.commit()
            return redirect("/posts")
        except Exception as ex:
            print(ex)
            return "An error occurred while updating!"
    else:
        return render_template("post_update.html", article=article)


@app.route("/posts")
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)


@app.route("/posts/<int:id_post>")
def post_detail(id_post):
    article = Article.query.get_or_404(id_post)
    return render_template("post_detail.html", article=article)


@app.route("/posts/<int:id_post>/delete")
def post_delete(id_post):
    article = Article.query.get_or_404(id_post)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect("/posts")
    except Exception as ex:
        print(ex)
        return "An error occurred while deleting!"


if __name__ == "__main__":
    app.run(debug=True)
