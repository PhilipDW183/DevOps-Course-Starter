import requests
import os
from dotenv import load_dotenv


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

    except E as err:

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


if __name__ == "__main__":

    load_dotenv()

    board_id = os.getenv("BOARD_ID")
    apikey = os.getenv("APIKEY")
    token = os.getenv("TOKEN")

    response = get_items(board_id, apikey, token)
    print(response)





