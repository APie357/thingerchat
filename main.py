import json
from flask import Flask, render_template, request, session, redirect, url_for
from flask_sock import Sock, Server, ConnectionClosed
import auth


app = Flask(__name__)
sock = Sock(app)

with open(".SECRET_KEY") as key:
    app.secret_key = key.read()

history: list[dict] = []
clients: list[Server] = []

server_sessions: dict[str, dict] = {}

def send(message: dict):
    global clients
    app.logger.info(f"[MESSAGE   ] {message['data']['channel']} {message['data']['username']}: {message['data']['message']}")
    history.append(message)
    new_clients = clients
    for client in clients:
        try:
            client.send(json.dumps(message))
        except ConnectionClosed:
            new_clients.remove(client)
    clients = new_clients


@app.route("/")
def index():
    if "session_uuid" in session:
        if session["session_uuid"] in server_sessions:
            return redirect(url_for("chat"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        _uuid = auth.login(request.form["name"], request.form["pass"])
        if _uuid is None:
            return render_template("login.html", message="Invalid login information."), 403
        _uuid = str(_uuid)
        server_sessions[_uuid] = {"username": request.form["name"]}
        session["session_uuid"] = _uuid
        return redirect(url_for("chat"))
    if "session_uuid" in session:
        if session["session_uuid"] in server_sessions:
            return redirect(url_for("chat"))
    return render_template("login.html", message="")


@app.route("/logout")
def logout():
    try:
        server_sessions.pop(session["session_uuid"])
        session.pop("session_uuid", default=None)
    except Exception:
        pass
    return redirect("login")


@app.route("/chat")
def chat():
    if "session_uuid" in session:
        if session["session_uuid"] in server_sessions:
            return render_template("chat.html")
    return redirect(url_for("login"))


@sock.route("/socket")
def socket(client: Server):
    app.logger.info(f"[NEW CLIENT] {server_sessions[session['session_uuid']]['username']}: "
            + f"{request.remote_addr} {request.user_agent}")
    clients.append(client)
    while client.connected:
        recv = client.receive(0)
        if recv is not None:
            try:
                message = json.loads(recv)
                if "type" in message and "data" in message:
                    if message["type"] == "send" and "message" in message["data"] and "channel" in message["data"]:
                        send({
                            "type": "new_message",
                            "data": {
                                "message": message["data"]["message"],
                                "username": server_sessions[session["session_uuid"]]["username"],
                                "channel": message["data"]["channel"]
                            }
                        })
            except Exception:
                continue


if __name__ == "__main__":
    app.run("0.0.0.0", 4200, True)
