import asyncio
import json
import pickle

import websockets
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout

import cast256
import rsa

base_url = "192.168.31.59"
messages_buffer = []
screen_limit = 30
server_data = {
    'active_users': 0,
    'users': []
}


async def listen(websocket, sim_key: bytes, session: PromptSession):
    global server_data
    async for msg in websocket:
        data = pickle.loads(msg)
        request_type = data['type']
        match request_type:
            case "message":
                payload = data['body']
                message = cast256.decrypt(payload, sim_key).decode()
                print(message)
            case 'info':
                server_data = data['body']
                session.app.invalidate()


async def send_messages(websocket, nickname, sim_key: bytes, session: PromptSession):
    while True:
        with patch_stdout():
            message = await session.prompt_async(
                f"{nickname}> ",
                bottom_toolbar=f"Active users: "
                               f"{server_data['active_users']} : "
                               f"{server_data['users']}",
                refresh_interval=0.5
            )
        message_encrypted = cast256.encrypt(f'{nickname}> {message}', sim_key)
        request = {'type': 'message', 'body': message_encrypted}
        try:
            await websocket.send(json.dumps(request))
        except:
            print("error sending message")


async def chat():
    nickname = input("Enter your name: ")
    print("Starting connection...")
    private_key, public_key = rsa.generate_keys()
    async with websockets.connect(f'ws://{base_url}:8000') as websocket:
        pkey_bytes = public_key.public_bytes(
            encoding=Encoding.DER,
            format=PublicFormat.SubjectPublicKeyInfo,
        )
        await websocket.send(pkey_bytes)
        sim_key_encrypted = await websocket.recv()
        confirm = {'type': 'accept', 'body': nickname}
        sim_key = rsa.decrypt(private_key, sim_key_encrypted)
        await websocket.send(pickle.dumps(confirm))
        print(f"Received cast256 key...")
        print("Established connection...")
        session = PromptSession()

        receive_msg_task = asyncio.create_task(listen(websocket, sim_key))
        send_messages_task = asyncio.create_task(send_messages(websocket, nickname, sim_key))
        await asyncio.gather(receive_msg_task, send_messages_task)


if __name__ == "__main__":
    asyncio.run(chat())
