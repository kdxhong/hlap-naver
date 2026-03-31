import os
from dotenv import load_dotenv

print(f"Current Working Directory: {os.getcwd()}")
print(f".env file exists: {os.path.exists('.env')}")

load_dotenv()

cid = os.getenv("NAVER_CLIENT_ID")
csec = os.getenv("NAVER_CLIENT_SECRET")

print(f"NAVER_CLIENT_ID found: {bool(cid)}")
if cid:
    print(f"NAVER_CLIENT_ID length: {len(cid)}")
print(f"NAVER_CLIENT_SECRET found: {bool(csec)}")
if csec:
    print(f"NAVER_CLIENT_SECRET length: {len(csec)}")
