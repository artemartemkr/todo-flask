from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///TodoApp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


def __repr__(self):
    return '<Article %r>' % self.id


@app.route('/posts')
@app.route('/')
def posts():
    article = Article.query.order_by(Article.created_at.desc()).all()
    return render_template("posts.html", article=article)


@app.route('/posts/<int:id>')
def posts_detail(id):
    article = Article.query.get(id)
    return render_template("posts_detail.html", article=article)


@app.route('/posts/<int:id>/delete')
def posts_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении произошла ошибка"


@app.route('/posts/<int:id>/patch', methods=['POST', 'GET'])
def post_patch(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "При реадктировании произошла ошибка"
    else:
        return render_template("post_patch.html", article=article)


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']

        article = Article(title=title, content=content)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавлении произошла ошибка"
    else:
        return render_template("create_article.html")


if __name__ == "__main__":
    app.run(debug=True)
