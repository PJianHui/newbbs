from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    abort,
)
from routes import *

from models.topic import Topic
from  models.board import Board

main = Blueprint('topic', __name__)

import uuid
csrf_tokens = {}
@main.route("/")
def index():
    board_id = int(request.args.get('board_id', -1))
    if board_id == -1:
        ms = Topic.all_delay()
    else:
        ms = Topic.find_all(board_id=board_id)
    token = str(uuid.uuid4())
    u = current_user()
    csrf_tokens['token'] = u.id
    bs = Board.all()
    return render_template("topic/index.html", ms=ms, token=token, bs=bs,u=u)

@main.route('/<int:id>')
def detail(id):
    m = Topic.get(id)
    user = m.user()
    board = m.board()
    return render_template('topic/detail.html', topic=m, user=user, board=board, )

@main.route("/add", methods= ["POST"])
def add():
    form =request.form
    u =current_user()
    m = Topic.new(form, user_id=u.id)
    return redirect(url_for('.detail', id=m.id))

@main.route("/delete")
def delete():
    id = int(request.args.get('id'))
    token = request.get('token')
    u = current_user()
    # 判断token 是否正确
    if token in csrf_tokens and csrf_tokens[token] == u.id:
        csrf_tokens.pop(token)
        if u is not None:
            print('删除 topic 用户是', u.id)
            Topic.delete(id)
            return redirect(url_for('.index'))
        else:
            abort(404)
    else:
        abort(403)

@main.route("/new")
def new():
    bs = Board.all()
    return render_template("topic/new.html", bs=bs)