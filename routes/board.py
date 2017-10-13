from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    abort,
)

from routes import *

from models.board import Board


main = Blueprint('board', __name__)


@main.route("/main")
def index():
    u = current_user()
    form = request.form
    if u.role == 1:
        m = Board.new(form)
        return render_template('board/admin_index.html')
    else:
        abort(404)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()
    if u.role == 1:
        m = Board.new(form)
        return redirect(url_for('topic.index'))
    else:
        abort(404)

@main.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    u = current_user()
    if u.role == 1:
        m = Board.find(title=title)
        m.delete()
        return redirect(url_for('topic.index'))
    else:
        abort(404)

