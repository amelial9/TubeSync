import asyncio
import websockets
import json
import time
import os
import threading
from dotenv import load_dotenv
from pypresence import Presence

load_dotenv()
client_id = os.getenv("DISCORD_CLIENT_ID")

RPC = None
YOUTUBE_ACTIVE = False
PORT = 3000

def try_connect_discord(client_id):
    try:
        rpc = Presence(client_id)
        rpc.connect()
        print("[TubeSync] Discord Rich Presence connected")
        return rpc
    except Exception as e:
        print(f"[TubeSync] Failed to connect: {e}")
        return None

if client_id:
    RPC = try_connect_discord(client_id)

def ensure_discord_connected():
    global RPC
    if RPC is None and client_id:
        RPC = try_connect_discord(client_id)

def discord_reconnect_loop():
    while True:
        ensure_discord_connected()
        time.sleep(10)

threading.Thread(target=discord_reconnect_loop, daemon=True).start()

def update_discord_presence(title, author, is_live=False, time_pos=0, duration=0):
    global RPC, YOUTUBE_ACTIVE

    if not RPC:
        print("[TubeSync] Discord not open.")
        return
    if not YOUTUBE_ACTIVE:
        print("[TubeSync] No YouTube tab open.")
        return

    def _update():
        try:
            activity = {
                "details": title,
                "large_image": "youtube_logo"
            }

            if is_live:
                activity["state"] = f"{author} – 🔴 Live"
            else:
                mins_pos, secs_pos = divmod(time_pos, 60)
                mins_dur, secs_dur = divmod(duration, 60)
                activity["state"] = (
                    f"{author} – {mins_pos:02d}:{secs_pos:02d}/{mins_dur:02d}:{secs_dur:02d}"
                )

            RPC.update(**activity)
            print(f"[TubeSync] Updated Discord: {activity['details']} | {activity['state']}")

        except Exception as e:
            print(f"[TubeSync] Failed to update Discord presence: {e}")

    threading.Thread(target=_update, daemon=True).start()

def clear_discord_presence():
    global RPC
    if not RPC:
        return

    def _clear():
        try:
            RPC.clear()
            print("[TubeSync] Discord presence cleared.")
        except Exception as e:
            print(f"[TubeSync] Failed to clear Discord presence: {e}")

    thread = threading.Thread(target=_clear)
    thread.daemon = True
    thread.start()

async def handle_connection(websocket):
    global YOUTUBE_ACTIVE
    YOUTUBE_ACTIVE = True
    print(f"[TubeSync] YouTube connected: {websocket.remote_address}")

    try:
        async for message in websocket:
            print("[TubeSync] Raw message:", message)
            try:
                data = json.loads(message)
                print("[TubeSync] Received playback data:")
                print(f"Title: {data.get('title')}")
                print(f"Author: {data.get('author')}")
                print(f"Time: {data.get('time')} / {data.get('duration')} sec")
                print(f"Live: {'Yes' if data.get('isLive') else 'No'}\n")

                title = data.get('title', 'Unknown')
                author = data.get('author', 'Unknown')
                is_live = data.get('isLive', False)
                time_pos = data.get('time', 0)
                duration = data.get('duration', 0)

                update_discord_presence(title, author, is_live, time_pos, duration)

            except json.JSONDecodeError:
                print("⚠️ Received invalid JSON:", message)

    except websockets.exceptions.ConnectionClosed:
        print("[TubeSync] YouTube disconnected.")
        YOUTUBE_ACTIVE = False
        clear_discord_presence()

async def main():
    print(f"[TubeSync] Starting server on ws://localhost:{PORT}")
    try:
        async with websockets.serve(handle_connection, "", PORT):
            await asyncio.Future()
    except KeyboardInterrupt:
        print("\n[TubeSync] Server shutting down")
    finally:
        if RPC:
            try:
                clear_discord_presence()
                RPC.close()
                print("[TubeSync] Discord Rich Presence disconnected.")
            except Exception as e:
                print(f"[TubeSync] Error closing Discord connection: {e}")

if __name__ == "__main__":
    asyncio.run(main())
