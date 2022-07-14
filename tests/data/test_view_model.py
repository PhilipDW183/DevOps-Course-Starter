from todo_app.data.view_model import ViewModel
from todo_app.data.trello_items import Item

def test_doing_items_property():

    item1 = Item("id1", "test task 1", "1234", "test task desc", "16-07-2022")
    item2 = Item("id2", "test task 2", "12345", "test task desc", "15-07-2022")
    item3 = Item("id3", "test task 3", "123456", "test task desc", "15-07-2022")

    items = [item1, item2, item3]

    list_targets = {"To Do": "1234",
                    "Doing": "12345",
                    "Done": "123456"}

    view_model = ViewModel(items, list_targets)

    doing_it_items = view_model.doing_items

    assert doing_it_items == [item2]
