import requests
import os
from dotenv import load_dotenv
from dateutil import parser

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


def get_items(board_id, api_key, token):
    """
    Get all action items on the trello board

    Inputs
        board_id: id of the board we want the items for
        api_key: api_key for accessing trello
        token: api token for accessing trello

    Returns
        response_json: a json of the response from the request
    """

    target_url = f"https://api.trello.com/1/boards/{board_id}/cards"

    params = {
        "key": api_key,
        "token": token
    }

    response = call_api(target_url, "GET", params)

    return response


def add_item(title, description, due_date, destination, api_key, token):
    """
    Adds a new item with the specified title to the session.

    Args
        title: The title of the item.
        description: description of the item
        due_date: due_date of the item
        api_key: api_key for accessing trello
        token: api token for accessing trello
        destination: target list id to add to

    Returns
        item: The saved item.
    """

    target_url = f"https://api.trello.com/1/cards"

    params = {
        "key": api_key,
        "token": token,
        "name": title,
        "idList": destination,
        "desc": description,
        "due": due_date
    }

    response = call_api(target_url, "POST", params)

    return response.get("id")


def change_item_status(card_id, destination, api_key, token):
    """Change item status to another list

    Args
        card_id: id of the item we want to change
        destination: where we want to change the item to
        api_key: api_key for accessing trello
        token: api token for accessing trello

    Output
        id: id of the update item
    """
    target_url = f"https://api.trello.com/1/cards/{card_id}"

    params = {
        "key": api_key,
        "token": token,
        "idList": destination
    }

    api_response = call_api(target_url, "PUT", params)

    return id


def remove_item(card_id, api_key, token):
    """
    Removes an existing item from the session. If no item matching the id then nothing is returned

    Args:
        card_id: item id to be removed
        api_key: api_key for accessing trello
        token: api token for accessing trello

    Returns:
        id: item id to be removed

    """
    target_url = f"https://api.trello.com/1/cards/{card_id}"

    params = {
        "key": api_key,
        "token": token
    }

    api_response = call_api(target_url, "DELETE", params)

    return card_id


def get_list_names(board_id, api_key, token):
    """Get a list of all list names within the trello board

    Args
        board_id: id of the board we are going to use
        api_key: trello api key
        token: trello token

    output
        target_lists: a list of all list ids from the trello board we are interested in
    """

    target_url = f"https://api.trello.com/1/boards/{board_id}/lists"

    params = {
        "key": api_key,
        "token": token
    }

    api_response = call_api(target_url, "GET", params)

    target_lists = {"To Do": None,
                    "Done": None}

    #loop over the lists to get the list names that we need
    for list in api_response:
        if list.get("name") in target_lists.keys():
            target_lists[list.get("name")] = list.get("id")

    for k, v in target_lists.items():
        if not v:
            raise Exception(f"No list named {k}. Please create a list with this name")

    return target_lists


if __name__ == "__main__":

    load_dotenv()

    board_id = os.getenv("BOARD_ID")
    api_key = os.getenv("API_KEY")
    token = os.getenv("TOKEN")

    board_lists = get_list_names(board_id, api_key, token)

    get_items_response = get_items(board_id,
                                   api_key,
                                   token)

    print(get_items_response)

    response = get_items("62cc1dd1e32d46579e3e2218",
              api_key,
              token)
    print(response)

    add_response = add_item("Create a new test item",
                            "This should create a new test item",
                            "2022-08-23",
                            api_key,
                            token)

    change_item_status(get_items_response[0].get("id"),
                       board_lists.get("done"),
                api_key,
                token)

    delete_response = remove_item(get_items_response[0].get("id"),
                                  api_key,
                                  token)





