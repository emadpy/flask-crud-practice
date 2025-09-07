from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)


with app.app_context():
    db.create_all()


@app.route("/", methods=["GET"])
def index():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.paginate(page=page, per_page=3)
    return render_template("index.html", posts=posts)


@app.route("/<int:post_id>", methods=["GET"])
def get_post_id(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", post=post)


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        new_post = Post(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for("index"))
    
    return render_template("create.html")


@app.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit(post_id):
    post = Post.query.get_or_404(post_id)

    if request.method == "POST":
        post.title = request.form["title"]
        post.content = request.form["content"]
        db.session.commit()

        return redirect(url_for("index"))
    
    return render_template("edit.html", post=post)


@app.route("/delete/<int:post_id>", methods=["POST"])
def delete(post_id):
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)