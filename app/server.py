import asyncio
import websockets
import json

PORT = 3000

async def handle_connection(websocket):
    print(f"[TubeSync] Client connected: {websocket.remote_address}")
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                print("[TubeSync] Received playback data:")
                print(f"Title: {data.get('title')}")
                print(f"Author: {data.get('author')}")
                print(f"Time: {data.get('time')} / {data.get('duration')} sec")
                print(f"Playing: {'Yes' if data.get('playing') else 'Paused'}\n")
            except json.JSONDecodeError:
                print("⚠️ Received invalid JSON:", message)
    except websockets.exceptions.ConnectionClosed:
        print("[TubeSync] Client disconnected.")

async def main():
    print(f"[TubeSync] Starting server on ws://localhost:{PORT}")
    async with websockets.serve(handle_connection, "localhost", PORT):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
