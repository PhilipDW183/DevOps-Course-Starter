from flask import Flask, render_template, url_for, redirect, request
from todo_app.data.session_items import get_item
from todo_app.data.trello_items import get_items, add_item, change_item_status, remove_item, Item, get_list_names
from dotenv import load_dotenv
import os


from todo_app.flask_config import Config

load_dotenv()

board_id = os.getenv("BOARD_ID")
api_key = os.getenv("API_KEY")
token = os.getenv("TOKEN")

app = Flask(__name__)
app.config.from_object(Config())

list_targets = get_list_names(board_id, api_key, token)


@app.route('/')
def index():
    items = get_items(board_id, api_key, token)
    items = [Item.from_trello_cards(item) for item in items]
    #clean date in each item if they have due date
    for item in items:
        if item.due_date:
            item.clean_date()

    return render_template("index.html", items=items, list_targets=list_targets)


@app.route('/create_new_task', methods=["POST"])
def create_new_task():
    item_title = request.form.get('todo')
    item_description = request.form.get("description")
    item_due_date = request.form.get("date")
    destination_list = list_targets["To Do"]
    add_item(item_title,
             item_description,
             item_due_date,
             destination_list,
             api_key,
             token)
    return redirect(url_for("index"))


@app.route('/complete_item/<id>')
def complete_item(id):
    destination_list = list_targets["Done"]
    complete_id = change_item_status(id, destination_list, api_key, token)
    return redirect(url_for("index"))


@app.route('/uncomplete_item/<id>')
def uncomplete_item(id):
    destination_list = list_targets["To Do"]
    uncomplete_id = change_item_status(id, destination_list, api_key, token)
    return redirect(url_for("index"))


@app.route('/delete_item/<id>')
def delete_item(id):
    remove_item(id, api_key, token)
    return redirect(url_for("index"))

