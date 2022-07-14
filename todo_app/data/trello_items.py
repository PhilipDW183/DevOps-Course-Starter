import requests
import os
from dotenv import load_dotenv
from dateutil import parser
from os import environ


class Item:

    def __init__(self, id, name, list_id, description, due_date):
        self.id = id
        self.name = name
        self.idList = list_id
        self.description = description
        self.due_date = due_date

    @classmethod
    def from_trello_cards(cls, card):
        return cls(card["id"],
                   card["name"],
                   card["idList"],
                   card["desc"],
                   card["due"])

    def clean_date(self):
        if self.due_date:
            trello_date = parser.parse(self.due_date)
            self.due_date = trello_date.date()


def build_url(endpoint):
    """Build the url with the desired endpoint for the trello api"""
    return "https://api.trello.com/1" + endpoint


def call_api(url, method, query, headers=None):
    """call the specified url with the specified call and paramaters

    Inputs
        url: url endpoint to be called
        params: parameters for the api call
        method: type of call to make to the url

    Raises
        Exception in the case of connection error

    Outputs
        response: json of the response
    """

    try:
        response = requests.request(
            method,
            url,
            headers=headers,
            params=query
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.HTTPError as http_err:

        print(f"HTTP error occurred: {http_err}")

    except Exception as err:

        print(f"Error occurred: {err}")


def get_items(board_id):
    """
    Get all action items on the trello board

    Inputs
        board_id: id of the board we want the items for

    Returns
        response_json: a json of the response from the request
    """

    target_url = build_url(f"/boards/{board_id}/cards")

    params = build_params()

    response = call_api(target_url, "GET", params)

    return response


def add_item(title, description, due_date, destination):
    """
    Adds a new item with the specified title to the session.

    Args
        title: The title of the item.
        description: description of the item
        due_date: due_date of the item
        destination: target list id to add to

    Returns
        item: The saved item.
    """

    target_url = build_url("/cards")

    extra_params = {
        "name": title,
        "idList": destination,
        "desc": description,
        "due": due_date
    }

    params = build_params(extra_params)

    response = call_api(target_url, "POST", params)

    return response.get("id")


def change_item_status(card_id, destination):
    """Change item status to another list

    Args
        card_id: id of the item we want to change
        destination: where we want to change the item to

    Output
        id: id of the update item
    """

    target_url = build_url(f"/cards/{card_id}")

    extra_params = {
        "idList": destination
    }

    params = build_params(extra_params)

    api_response = call_api(target_url, "PUT", params)

    return id


def remove_item(card_id):
    """
    Removes an existing item from the session. If no item matching the id then nothing is returned

    Args:
        card_id: item id to be removed

    Returns:
        id: item id to be removed

    """

    target_url = build_url(f"/cards/{card_id}")

    params = build_params()

    api_response = call_api(target_url, "DELETE", params)

    return card_id


def get_list_names(board_id):
    """Get a list of all list names within the trello board

    Args
        board_id: id of the board we are going to use

    output
        target_lists: a list of all list ids from the trello board we are interested in
    """

    target_url = build_url(f"/boards/{board_id}/lists")

    params = build_params()

    api_response = call_api(target_url, "GET", params)

    target_lists = {"To Do": None,
                    "Doing": None,
                    "Done": None}

    #loop over the lists to get the list names that we need
    for list in api_response:
        if list.get("name") in target_lists.keys():
            target_lists[list.get("name")] = list.get("id")

    for k, v in target_lists.items():
        if not v:
            raise Exception(f"No list named {k}. Please create a list with this name")

    return target_lists


def get_auth_params():
    return {"key": environ.get("API_KEY"), "token": environ.get("TOKEN")}


def build_params(params={}):
    full_params = get_auth_params()
    full_params.update(params)
    return full_params
