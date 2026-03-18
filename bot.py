import requests
import time

VK_TOKEN = "PASTE_TOKEN_HERE"
GROUP_ID = 123456789

def send_vk(user_id, message):
    requests.post("https://api.vk.com/method/messages.send", params={
        "user_id": user_id,
        "message": message,
        "random_id": 0,
        "access_token": VK_TOKEN,
        "v": "5.199"
    })

def get_long_poll():
    response = requests.get("https://api.vk.com/method/groups.getLongPollServer", params={
        "access_token": VK_TOKEN,
        "v": "5.199",
        "group_id": GROUP_ID
    }).json()

    return response["response"]

def run():
    server_data = get_long_poll()
    server = server_data["server"]
    key = server_data["key"]
    ts = server_data["ts"]

    while True:
        response = requests.get(server, params={
            "act": "a_check",
            "key": key,
            "ts": ts,
            "wait": 25
        }).json()

        if "updates" in response:
            for update in response["updates"]:
                if update["type"] == "message_new":
                    msg = update["object"]["message"]
                    user_id = msg["from_id"]

                    send_vk(user_id, "Привет! 👋 Напиши, что хочешь напечатать на 3D-принтере.")

        ts = response["ts"]

if __name__ == "__main__":
    run()
