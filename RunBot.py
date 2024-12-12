

# Install required packages

# pip install requests asyncio web3 hexbytes websocket-client --break-system-packages

import os
import requests
import os
import asyncio
import random
import socket
import struct
import uuid
import os
from web3 import Web3
from hexbytes import HexBytes
from eth_account.messages import encode_defunct
import websocket
import threading
import time

BOOL_USE_PRINT = False
def is_ssh():
    return "SSH_CONNECTION" in os.environ or "SSH_TTY" in os.environ

def ssh_print(text, *args):
    if BOOL_USE_PRINT:
        print(text, *args)
BOOL_USE_PRINT = is_ssh()

# if is_ssh():
#     run_command="sudo systemctl stop apintio_bot_twitch.service"
#     ssh_print("Stopping the service while we run ssh code with command:", run_command)
#     os.system(run_command)



# Debian: /lib/systemd/system/apintio_bot_twitch.service
# Learn: https://youtu.be/nvx9jJhSELQ?t=279s

# sudo nano /lib/systemd/system/apintio_bot_twitch.service
"""
[Unit]
Description=Twitch Bot Auth
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /git/twitch_bot/RunBot.py
Restart=always
User=root
WorkingDirectory=/git/twitch_bot

[Install]
WantedBy=multi-user.target
"""
#1h
# sudo nano /etc/systemd/system/apintio_bot_twitch.timer
"""
[Unit]
Description=Twitch Bot Auth time manager

[Timer]
OnBootSec=0min
OnUnitActiveSec=10s

[Install]
WantedBy=timers.target
"""
# Learn: https://youtu.be/nvx9jJhSELQ?t=368
# cd /lib/systemd/system/
# sudo systemctl daemon-reload
# sudo systemctl enable apintio_bot_twitch.service
# chmod +x /git/twitch_bot/RunBot.py
# sudo systemctl enable apintio_bot_twitch.service
# sudo systemctl start apintio_bot_twitch.service
# sudo systemctl status apintio_bot_twitch.service
# sudo systemctl stop apintio_bot_twitch.service
# sudo systemctl restart apintio_bot_twitch.service
# sudo systemctl list-timers | grep apintio_bot_twitch


def read_or_create_file(file_path, default_content=""):
    
    # create directory if not there
    string_folder_path = os.path.dirname(file_path)
    if not os.path.exists(string_folder_path):
        os.makedirs(string_folder_path)
    
    # Check if the file exists
    if not os.path.exists(file_path):
        # Create the file with default content
        with open(file_path, "w") as f:
            f.write(default_content)
    
    # Read the content from the file
    with open(file_path, "r") as f:
        return f.read().strip()

client_id_path = "/token/twitch_bot_client_id.txt"
client_access_token_path = "/token/twitch_bot_access_token.txt"
CLIENT_ID =read_or_create_file(client_id_path, "your_twitch_client_id")
CLIENT_ACCESS_TOKEN= read_or_create_file(client_access_token_path, "your_twitch_token")









# Where should we store the verified users twithc_id|public_address
string_where_to_store_verified_user = "/git/metamask_users/twitch"


def verify_signature_from_text(text, splitter="|"):
    splitted = text.split(splitter)
    if len(splitted) == 3:
        return verify_signature(splitted[0], splitted[1], splitted[2])
    return False

def verify_signature(message, public_address, signed_message):
    w3 = Web3(Web3.HTTPProvider(""))
    mesage= encode_defunct(text=message)
    address_recovered = w3.eth.account.recover_message(mesage,signature=HexBytes(signed_message))
    ssh_print(address_recovered+" Recoverd vs Claim +"+public_address)
    is_verified = address_recovered == public_address
    return is_verified

def record_author_as_meta_mask_user_verified(author_id, public_address):
    ssh_print(f"Recorded user {author_id} as verified with public address {public_address}")
    if not os.path.exists(string_where_to_store_verified_user):
        os.makedirs(string_where_to_store_verified_user)
    with open(f"{string_where_to_store_verified_user}/{author_id}.txt", "w") as f:
        f.write(public_address)
    ssh_print("Path:", os.path.abspath(f"{string_where_to_store_verified_user}/{author_id}.txt"))
    


WS_SERVER = "wss://irc-ws.chat.twitch.tv:443"


## Generate a full access token: 
## https://twitchtokengenerator.com/quick/BhipWavsJL

## Generate a access token I want, Eloi: 
# https://twitchtokengenerator.com/quick/AIUO4Kwkch


# Authentication details

# https://eloistree.github.io/SignMetaMaskTextHere/index.html?q=apintio
# apintio|0xFEEAcdE5d735B8b347D9BBF8fBd02FEd153b564A|0xd381e82f743359a64552437a5d1ffebca38e095590db20a614a55a700d978e7865906179929afc621f6f561d8f91313abc4c74f3057bc1edb54e302f8fbfcef21c
# EloiTeaching|0xFEEAcdE5d735B8b347D9BBF8fBd02FEd153b564A|0xa4e04657d375c83f6e412b41a6f96fd214e5f7992fcadd207183dd8e96efa65736e7a9db85ea326b319fda150f0198621aeaa59713d5222e7688b162304dc53d1c


# https://twitchtokengenerator.com/?code=9w2p1cxleef6elv2t6tq30mgqt6tsn&scope=chat%3Aread+chat%3Aedit+whispers%3Aread+whispers%3Aedit+user%3Amanage%3Awhispers+user%3Aread%3Achat&state=frontend%7CdE40d3lPK3NadmxHWlpCaDV6RWtKUT09

USERNAME = "EloiTeacher"  # Twitch username
CHANNEL = "eloiteaching"  # Include the hash (#) before the channel name



# def whisper(ws, user, message):
#     ws.send(f"PRIVMSG #{USERNAME} :.w {user} {message}")



def get_user_id_from_name(user_name):
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {CLIENT_ACCESS_TOKEN}"
    }
    # WARNING: API CALL ARE LIMITED IN RATE AND QUANTITY
    # YOU HAVE TO USE IT IN A QUEUE AND WISELY TO AVOID BEING "BANNED"
    # https://dev.twitch.tv/docs/api/guide/#twitch-rate-limits
    url = f"https://api.twitch.tv/helix/users?login={user_name}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        if user_data["data"]:
            user_info = user_data["data"][0]
            # print(f"User ID: {user_info['id']}")
            # print(f"Username: {user_info['login']}")
            # print(f"Display Name: {user_info['display_name']}")
            # print(f"Broadcaster Type: {user_info['broadcaster_type']}")
            # print(f"Description: {user_info['description']}")
            # print(f"Profile Image URL: {user_info['profile_image_url']}")
            # print(f"View Count: {user_info['view_count']}")
            # print(f"Account Created At: {user_info['created_at']}")
            return user_info['id']
        else:
            ssh_print("User not found.")
    else:
        ssh_print(f"Error: {response.status_code}")
        ssh_print(response.json())
    return None


def read_store_public_key(user_id):
    string_file = f"{string_where_to_store_verified_user}/{user_id}.txt"
    if not os.path.exists(string_file):
        return None
    
    public_key =""
    with open(string_file, "r") as f:
        public_key = f.read().strip()
    return public_key
    
    

def on_message(ws, message):
    """Callback for when a message is received."""
    ssh_print(f"Received: {message}")
    
    message = message.strip()
    message = message.strip(":")
    #apintio!apintio@apintio.tmi.twitch.tv PRIVMSG #eloiteaching :test
    mark_index=message.find("!")
    first_comma_index=message.find(":")
    user_name = message[0:mark_index].lower()
    user_message= message[first_comma_index+1:].strip()
    ssh_print(f"User name:{user_name}")
    ssh_print(f"User message:{user_message}")

    
    if user_message.lower().find(user_name.lower()) == 0:
        ssh_print("User name found at start")
        if message.find("|")>0:
            ssh_print ("MetaMask Signed requested")
            if verify_signature_from_text(user_message):
                ssh_print("Signature verified !!! :)")
                ws.send(f"PRIVMSG #{CHANNEL} :Signature verified 🎊.")
                user_id = get_user_id_from_name(user_name)
                if user_id:
                    record_author_as_meta_mask_user_verified(user_id, user_message.split("|")[1])
                    ws.send(f"PRIVMSG #{CHANNEL} :User {user_name}({user_id}) has been verified and added")
            else:
                ssh_print("Signature not verified :(")
                
    elif user_message=="!PING":
        send_message_pong(ws)
        
    elif user_message=="!hello":
        send_message(ws,"Hello World!")
        
    elif user_message=="!time":
        send_message(ws, time.ctime())
        
    elif user_message=="!delete_key":
        user_id = get_user_id_from_name(user_name)
        string_file = f"{string_where_to_store_verified_user}/{user_id}.txt"
        if os.path.exists(string_file):
            os.remove(string_file)
            send_message(ws,f"Deleted:{user_name}({user_id})>🦊>None")
        
    elif user_message=="!key":
        # To remote later when I have the queue in place for API calls
        user_id = get_user_id_from_name(user_name)
        public_key= read_store_public_key(user_id)
        if public_key is not None: 
            send_message(ws,f"Stored:{user_name}({user_id})>🦊>{public_key}")
        else :
            send_message(ws,f"Stored:{user_name}({user_id})>🦊>")
    elif user_message=="!restart_bot" and (user_name=="apintio" or user_name=="eloiteaching"):
        exit()
        ws.close()
            
    else:
            
        try:
            int_value = int(user_message)
            ssh_print(f"User int command: {int_value}")
        except:
            a=0
        
    
            

def send_message(ws, message):
        
    ws.send(f"PRIVMSG #{CHANNEL} :{message}")
    
def send_message_hello_world(ws):
    send_message(ws,">> Server Start\nHello World!\n🤖🧙‍♂️🦊")
    
def send_message_bye_world(ws):
    send_message(ws,"Server Stop 🛑👋!")
    
def send_message_pong(ws):
    send_message(ws,"PONG")
        

def on_error(ws, error):
    """Callback for errors."""
    ssh_print(f"Error: {error}")
    send_message_bye_world(ws)


def on_close(ws, close_status_code, close_msg):
    """Callback for when the WebSocket is closed."""
    ssh_print(f"Closed: {close_status_code}, {close_msg}")
    send_message_bye_world(ws)


    
def on_open(ws):
    """Callback for when the WebSocket connection is established."""
    ssh_print("Connection opened")
    ssh_print(f"PASS oauth:{CLIENT_ACCESS_TOKEN[0:6]}")
    ssh_print(f"NICK {USERNAME}")
    ssh_print(f"JOIN #{CHANNEL}")
    ws.send(f"PASS oauth:{CLIENT_ACCESS_TOKEN}")
    ws.send(f"NICK {USERNAME}")
    ws.send(f"JOIN #{CHANNEL}")
    send_message_hello_world(ws)
    
    
    # Keep the connection alive (send PING periodically)
    def keep_alive():
        while True:
            time.sleep(60)  # Twitch requires PING every 5 minutes, but doing it every 60s for safety
            ws.send("PING :tmi.twitch.tv")
    
    
    threading.Thread(target=keep_alive, daemon=True).start()

if __name__ == "__main__":
    # Create WebSocketApp and set callbacks
    ws = websocket.WebSocketApp(
        WS_SERVER,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.on_open = on_open
    
    # Run WebSocketApp
    ws.run_forever()



#--------------------------------




## Was close but did not succed to get the token correctly.
## I will use the token from the twitchtokengenerator.com every then and then.
# recover_token =""
# url = "https://id.twitch.tv/oauth2/token"
# payload = {
#     "client_id": CLIENT_ID,
#     "client_secret": CLIENT_SECRET,
#     "grant_type": "client_credentials",
#     "scope": "chat:read chat:edit whispers:read whispers:edit"
# }

# # Make the POST request to get the access token
# response = requests.post(url, data=payload)

# # Check if the request was successful
# if response.status_code == 200:
#     # Parse the response to extract the access token
#     token_info = response.json()
#     recover_token = token_info['access_token']
#     print("Access Token:", recover_token)
# else:
#     print("Failed to get the token:", response.status_code, response.text)