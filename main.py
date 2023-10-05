from flask import Flask, redirect, render_template
from flask_sock import Sock, Server
import auth
import json


app = Flask(__name__)
sock = Sock(app)

@app.route("/")
def chat():
    return render_template("chat.html")


@sock.route("/socket")
def socket(ws: Server):
    while ws.connected:
        recv = ws.receive()
        try:
            message = json.loads(recv)
            if "type" in message and "data" in message:
                if message["type"] == "send" and "message" in message["data"]:
                    ws.send(json.dumps({
                        "type": "new_message",
                        "data": {
                            "message": message["data"]["message"],
                            "username": "APie357"
                        }
                    }))
        except Exception:
            continue


if __name__ == "__main__":
    app.run("0.0.0.0", 4200, True)
