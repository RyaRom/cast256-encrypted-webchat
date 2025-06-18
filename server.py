import asyncio
import json
import pickle

import websockets
from cryptography.hazmat.primitives import serialization
from websockets import ServerConnection

import cast256
import rsa

connected_clients = dict()
server_info = {
    'active_users': 0,
    'users': []
}


async def handle_client(websocket: ServerConnection):
    user = None
    try:
        host, port = websocket.remote_address

        user = await init_connection(websocket)
        await send_info(server_info)
        async for msg in websocket:
            request = json.loads(msg)
            print(f"{host}:{port}: received: {request}")
            request_type = request["type"]
            match request_type:
                case "message":
                    await handle_message(websocket, request)
    except websockets.exceptions.ConnectionClosedError as e:
        print("Connection closed")
        raise e
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if user:
            print(f"Closing session for {user}")
            delete_user(user)
            await send_info(server_info)
        connected_clients.pop(websocket, None)


async def init_connection(websocket: ServerConnection):
    key_bytes = await websocket.recv()
    print("Received public key")
    pkey = serialization.load_der_public_key(key_bytes)
    sim_key = cast256.random_key()
    connected_clients[websocket] = sim_key
    encrypted = rsa.encrypt(pkey, sim_key)
    await websocket.send(encrypted)
    accept = pickle.loads(await websocket.recv())
    nickname = accept['body']
    add_user(nickname)
    return nickname


def add_user(nickname):
    server_info["active_users"] += 1
    server_info["users"].append(nickname)


def delete_user(nickname):
    server_info["active_users"] -= 1
    server_info["users"].remove(nickname)


async def handle_message(websocket: ServerConnection, request):
    key = connected_clients[websocket]
    message = cast256.decrypt(request["body"], key)
    print(f"got message {message}")
    await asyncio.gather(*[
        send_encrypted_message(ws, key, 'message', message)
        for ws, key in list(connected_clients.items())
        if ws != websocket
    ])


async def send_encrypted_message(
        ws: ServerConnection,
        key,
        msg_type: str,
        body):
    try:
        print(f'sending {body} to {ws.remote_address}')
        encrypted = cast256.encrypt(body, key)
        msg = {'type': msg_type, 'body': encrypted}
        await ws.send(pickle.dumps(msg))
    except websockets.exceptions.ConnectionClosed:
        print(f"Client {ws.remote_address} disconnected during send")
        connected_clients.pop(ws, None)
    except Exception as e:
        print(f"Error sending to {ws.remote_address}: {e}")


async def send_info(userinfo):
    await asyncio.gather(*[
        send_encrypted_message(ws, key, 'info', userinfo)
        for ws, key in list(connected_clients.items())
    ])


async def main():
    print("Started listening...")
    server = await websockets.serve(handle_client, '0.0.0.0', 8000)
    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
