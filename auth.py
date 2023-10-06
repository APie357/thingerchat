import base64
import uuid
import json
import bcrypt

with open(".SECRET_KEY") as s:
    salt = base64.b64decode(s.read())
with open("users.json") as f:
    users = json.loads(f.read())

def login(username: str, password: str):
    if username in users:
        if bcrypt.checkpw(password.encode(), base64.b64decode(users[username]["password"])):
            return uuid.uuid4()
    return None
