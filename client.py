import asyncio
import json
import pickle

import websockets
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout

import cast256
import rsa

base_url = "cutegirlshub.tech"
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
        payload: bytes = cast256.decrypt(data['body'], sim_key)
        match request_type:
            case "message":
                print(payload.decode())
            case 'info':
                server_data = pickle.loads(payload)
                session.app.invalidate()
            case 'buffer':
                messages = json.loads(payload)
                for message in messages:
                    print(message)


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
        sim_key = rsa.decrypt(private_key, sim_key_encrypted)
        print(f"Received cast256 key...")
        print("Established connection...")
        session = PromptSession()
        confirm = {'type': 'accept', 'body': nickname}
        await websocket.send(pickle.dumps(confirm))

        receive_msg_task = asyncio.create_task(listen(websocket, sim_key, session))
        send_messages_task = asyncio.create_task(send_messages(
            websocket, nickname, sim_key, session))
        await asyncio.gather(receive_msg_task, send_messages_task)



if __name__ == "__main__":
    asyncio.run(chat())
