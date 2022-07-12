import requests
import os
from dotenv import load_dotenv


class Item:

    def __init__(self, id, name, list_id):
        self.id = id
        self.name = name
        self.idList = list_id

    @classmethod
    def from_trello_cards(cls, card):
        return cls(card["id"], card["name"], card["idList"])


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
        return response.json()

    except Exception as err:

        raise Exception("Connection error. Please check parameters and try again", err)


def get_items(board_id, apikey, token):
    """
    Get all action items on the trello board

    Inputs
        board_id: id of the board we want the items for
        apikey: apikey for accessing trello
        token: api token for accessing trello

    Returns
        response_json: a json of the response from the request
    """

    target_url = f"https://api.trello.com/1/boards/{board_id}/cards"

    params = {
        "key": apikey,
        "token": token
    }

    response = call_api(target_url, "GET", params)

    return response


def add_item(title, apikey, token):
    """
    Adds a new item with the specified title to the session.

    Args
        title: The title of the item.
        apikey: apikey for accessing trello
        token: api token for accessing trello

    Returns
        item: The saved item.
    """

    target_url = f"https://api.trello.com/1/cards"

    params = {
        "key": apikey,
        "token": token,
        "name": title,
        #idList hardcoded for now as we are only adding to one list
        "idList": "62cc1a1f3eac6c0953e9df48"
    }

    response = call_api(target_url, "POST", params)

    return response.get("id")


def finish_item(card_id, apikey, token):
    """
    Changes and item to complete

    Args
        card_id: id of the item we want to update
        apikey: apikey for accessing trello
        token: api token for accessing trello

    Output
        id: id of the updated item
    """
    target_url = f"https://api.trello.com/1/cards/{card_id}"

    params = {
        "key": apikey,
        "token": token,
        "idList": "62cc1a1f3eac6c0953e9df4a"
    }

    api_response = call_api(target_url, "PUT", params)

    return id


def remove_item(card_id, apikey, token):
    """
    Removes an existing item from the session. If no item matching the id then nothing is returned

    Args:
        card_id: item id to be removed
        apikey: apikey for accessing trello
        token: api token for accessing trello

    Returns:
        id: item id to be removed

    """
    target_url = f"https://api.trello.com/1/cards/{card_id}"

    params = {
        "key": apikey,
        "token": token
    }

    api_response = call_api(target_url, "DELETE", params)

    return card_id


if __name__ == "__main__":

    load_dotenv()

    board_id = os.getenv("BOARD_ID")
    apikey = os.getenv("APIKEY")
    token = os.getenv("TOKEN")

    get_items_response = get_items(board_id, apikey, token)
    print(get_items_response)

    # add_response = add_item("Try again", apikey, token)
    # print(add_response)

    # finish_item(get_items_response[0].get("id"), apikey, token)

    delete_response = remove_item(get_items_response[0].get("id"), apikey, token)
    print(delete_response)





