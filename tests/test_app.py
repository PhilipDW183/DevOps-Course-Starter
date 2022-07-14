import pytest
from dotenv import load_dotenv, find_dotenv
from todo_app import app
import os
import requests

fake_cards = [{
    "id": "1",
    "name": "test1",
    "idList": "1",
    "desc": "test1",
    "due": "2022-06-07"
}, {
    "id": "2",
    "name": "test2",
    "idList": "1",
    "desc": "test2",
    "due": "2022-06-07"
}, {
    "id": "3",
    "name": "test3",
    "idList": "2",
    "desc": "test3",
    "due": "2022-06-07"
}, {
    "id": "4",
    "name": "test4",
    "idList": "3",
    "desc": "test3",
    "due": "2022-06-07"
}]

fake_lists = [{
    'id': '1',
    'name': 'To Do',
    'cards': [{'id': '456', 'name': 'Test card'}]
},
    {
        'id': '2',
        'name': 'Doing',
        'cards': [{'id': '456', 'name': 'Test card'}]
    },
    {
        'id': '3',
        'name': 'Done',
        'cards': [{'id': '456', 'name': 'Test card'}]
    }]


@pytest.fixture
def client(monkeypatch):
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    monkeypatch.setattr("requests.request", stub)

    # Create the new app.
    test_app = app.create_app()

    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client


class StubResponse:
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data

    def json(self):
        return self.fake_response_data

    @staticmethod
    def raise_for_status():
        return None


# Stub replacement for requests.get(url)
def stub(method, url, headers, params={}):
    test_board_id = os.environ.get('BOARD_ID')
    base_url = "https://api.trello.com/1"

    fake_response_data = None
    if url == f'{base_url}/boards/{test_board_id}/lists':
        print("url worked")
        fake_response_data = fake_lists
        return StubResponse(fake_response_data)

    if url == f"{base_url}/boards/{test_board_id}/cards":
        fake_response_data = fake_cards
        return StubResponse(fake_response_data)

    raise Exception(f'Integration test did not expect URL "{url}"')


def test_index_page(monkeypatch, client):
    # this replaces any call to requests.get with our own function
    print("does monkeypath work")
    response = client.get('/')

    assert response.status_code == 200
