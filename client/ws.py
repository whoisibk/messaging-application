import websockets, asyncio
from fastapi import WebSocket

"""Client-side program to handle websocket connections for real-time messaging."""



def websocket_connection_handler(url: str):
    """Establish and manage a websocket connection to the given URL.

    Args:
        url (str): The websocket server URL to connect to.
    """
    
    async def connect():
        
        # we can use 'async with' for cleaner code, but keeping it simple here
        try:
            # connect to the websocket server
            client_ws = websockets.connect(url)
            print(f"Connected to {url}")

            # handle sending and receiving messages concurrently
            await asyncio.gather(
                receive_messages(client_ws),
                send_message(client_ws)
            )

        except websockets.ConnectionClosed:
            print("Connection closed")
        
        # manually ensure the connection is closed properly, async would rather handle this automatically
        finally:
            client_ws.close()

    return connect    


async def receive_messages(websocket: WebSocket):
    """Receive messages from the websocket server."""

    # continuously listen for messages
    while True:
        message = await websocket.recv()
     
        # receive json from the server


        print(f"Received message: {message}")


async def send_message(websocket):
    """Send a message to the websocket server.

    Args:
        websocket: The websocket connection.
        message (str): The message to send.
    """

    while True:
        message = await input("Enter message to send: ")
        await websocket.send(message)
        print(f"You: {message}")
    
