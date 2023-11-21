
from apis import *
from get_klines import requests
def send_to_telegram(message):

    apiToken = API_TOKEN
    chatID = CHAT_ID
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
    message = str(message)

    try:
        response = requests.post(
            apiURL, json={'chat_id': chatID, 'text': message, 'parse_mode': 'html'})
    except Exception as e:
        print(e)