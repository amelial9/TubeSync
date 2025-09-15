from pypresence import Presence
import time
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("DISCORD_CLIENT_ID")
RPC = Presence(client_id)
RPC.connect()

print("Testing Discord Rich Presence")

RPC.update(
    state="vibing 🪩",
    details="Amelia testing Rich Presence",
    start=time.time()
)

time.sleep(10)
RPC.clear()
print("✅ Presence cleared")