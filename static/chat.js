if (!("WebSocket" in window)) { while (true) { alert("WebSockets aren't supported by your browser."); } }

var chatarea = document.getElementById("chatarea");
var sendtext = document.getElementById("sendtext");
var socket = new WebSocket("ws://127.0.0.1:4200/socket");

sendtext.addEventListener("keydown", (event) => {
    if (event.key == "Enter") {
        if (sendtext.value != "") {
            sendMessage(sendtext.value);
            sendtext.value = "";
        }
    }
});

function sendMessage(message) {
    var send = {
        "type": "send",
        "data": {
            "message": message
        }
    };
    socket.send(JSON.stringify(send));
}

socket.onmessage = (recv) => {
    var message = JSON.parse(recv.data);
    if (message["type"] == "new_message") {
        chatarea.value = `${chatarea.value}${message["data"]["username"]}: ${message["data"]["message"]}\n`;
    }
}

