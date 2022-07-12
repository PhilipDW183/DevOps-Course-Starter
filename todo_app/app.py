from flask import Flask, render_template, url_for, redirect, request
from todo_app.data.session_items import get_item, remove_item
from todo_app.data.trello_items import get_items, add_item, finish_item
from dotenv import load_dotenv
import os


from todo_app.flask_config import Config

load_dotenv()

board_id = os.getenv("BOARD_ID")
apikey = os.getenv("APIKEY")
token = os.getenv("TOKEN")

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    items = get_items(board_id, apikey, token)
    return render_template("index.html", items=items)


@app.route('/create_new_task', methods=["POST"])
def create_new_task():
    new_item = request.form.get('todo')
    add_item(new_item, apikey, token)
    return redirect(url_for("index"))


@app.route('/complete_item/<id>')
def complete_item(id):
    complete_id = finish_item(id, apikey, token)
    return redirect(url_for("index"))


@app.route('/delete_item/<id>')
def delete_item(id):
    remove_item(id)
    return redirect(url_for("index"))

