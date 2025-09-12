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
if client_id:
    RPC = Presence(client_id)
    RPC.connect()
    print("[TubeSync] Discord Rich Presence connected!")
else:
    print("[TubeSync] No Discord Client ID found. Rich Presence disabled.")

def update_discord_presence(title, author, playing, force_update=False):
    """Thread-safe function to update Discord Rich Presence
    
    Args:
        title: Song title
        author: Song author
        playing: Whether currently playing
        force_update: If True, will replace existing Discord activity
    """
    if not RPC:
        return
    
    def _update():
        try:
            if not force_update:
                print("[TubeSync] Note: Discord Rich Presence will replace your current activity.")
                print("[TubeSync] Set force_update=True to override existing activities.")
                return
            
            if playing:
                RPC.update(
                    state=f"by {author}",
                    details=f"🎵 {title}",
                    start=time.time()
                )
                print(f"[TubeSync] Updated Discord: Now playing {title} by {author}")
            else:
                RPC.update(
                    state=f"by {author}",
                    details=f"⏸️ {title} (Paused)",
                    start=time.time()
                )
                print(f"[TubeSync] Updated Discord: Paused {title} by {author}")
        except Exception as e:
            print(f"[TubeSync] Failed to update Discord presence: {e}")
    
    thread = threading.Thread(target=_update)
    thread.daemon = True
    thread.start()

def clear_discord_presence():
    """Thread-safe function to clear Discord Rich Presence"""
    if not RPC:
        return
    
    def _clear():
        try:
            RPC.clear()
        except Exception as e:
            print(f"[TubeSync] Failed to clear Discord presence: {e}")
    
    thread = threading.Thread(target=_clear)
    thread.daemon = True
    thread.start()

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
                
                title = data.get('title', 'Unknown')
                author = data.get('author', 'Unknown')
                playing = data.get('playing', False)
                force_update = data.get('force_discord_update', False)
                update_discord_presence(title, author, playing, force_update)
                        
            except json.JSONDecodeError:
                print("⚠️ Received invalid JSON:", message)
    except websockets.exceptions.ConnectionClosed:
        print("[TubeSync] Client disconnected.")
        clear_discord_presence()

async def main():
    print(f"[TubeSync] Starting server on ws://localhost:{PORT}")
    try:
        async with websockets.serve(handle_connection, "localhost", PORT):
            await asyncio.Future()
    except KeyboardInterrupt:
        print("\n[TubeSync] Server shutting down...")
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
