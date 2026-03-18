import requests
import time

VK_TOKEN = "vk1.a.ahhvtF0Xwt2FDQRbAGWILiMyB5FKx4kM56faEc_H0tI6Qg_sIGow3H0d-dXBI3My8BVmtVWrTfzZvrvQaFry_6dN06mCyeh6zvJp6tY5caKEhvqqZ14Zlm-eM4YWnjqONukBmIAeQnay3VatF8Xkh3LW76AbAOy2Ge9QqiO34Lr8_IRH0upKZ1Gv_-phGO2-h1zr6GSiCztBGJLVFNlLuA"
GROUP_ID = 236787443

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
