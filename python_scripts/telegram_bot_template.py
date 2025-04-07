import requests

TELEGRAM_TOKEN="YOUR TELEGRAM TOKEN" # obtain from bot father

def send_message(message): # sends a message
    chat_id = "YOUR CHAT ID"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    results = requests.get(url).json() # this sends the message
    print(results)
    return results['ok']

while True:
    # do something
    send_message("YOUR DATA")