from todo_app.data.view_model import ViewModel
from todo_app.data.trello_items import Item
import pytest


@pytest.fixture
def items_fixture():

    item1 = Item("id1", "test task 1", "1234", "test task desc", "16-07-2022")
    item2 = Item("id2", "test task 2", "12345", "test task desc", "15-07-2022")
    item3 = Item("id3", "test task 3", "123456", "test task desc", "15-07-2022")

    items = [item1, item2, item3]

    return items


@pytest.fixture
def list_targets_fixture():

    list_targets = {"To Do": "1234",
                    "Doing": "12345",
                    "Done": "123456"}

    return list_targets


@pytest.fixture
def view_model_fixture(items_fixture, list_targets_fixture):

    view_model = ViewModel(items_fixture, list_targets_fixture)

    return view_model


def test_to_do_items_property(items_fixture, view_model_fixture):

    to_do_items = view_model_fixture.to_do_items

    assert to_do_items == [items_fixture[0]]


def test_doing_items_property(items_fixture, view_model_fixture):

    doing_items = view_model_fixture.doing_items

    assert doing_items == [items_fixture[1]]


def test_done_items_property(items_fixture, view_model_fixture):

    done_items = view_model_fixture.done_items

    assert done_items == [items_fixture[2]]
