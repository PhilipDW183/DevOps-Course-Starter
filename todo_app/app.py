from flask import Flask, render_template, url_for, redirect, request
from todo_app.data.session_items import get_items, add_item, save_item, get_item, remove_item


from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    items = get_items()
    return render_template("index.html", items=items)


@app.route('/create_new_task', methods=["POST"])
def create_new_task():
    new_item = request.form.get('todo')
    add_item(new_item)
    return redirect(url_for("index"))


@app.route('/complete_item/<id>')
def complete_item(id):
    item_to_complete = get_item(id)
    item_to_complete["status"] = "Completed"
    save_item(item_to_complete)
    return redirect(url_for("index"))


@app.route('/delete_item/<id>')
def delete_item(id):
    remove_item(id)
    return redirect(url_for("index"))

