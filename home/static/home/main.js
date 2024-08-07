const roomName = JSON.parse(
  document.getElementById("json-roomname").textContent
);
const username = JSON.parse(
  document.getElementById("json-username").textContent
);

const chatSocket = new WebSocket(
  "ws://" + window.location.host + "/ws/chatroom/" + roomName + "/"
);

chatSocket.onmessage = function (e) {
  const data = JSON.parse(e.data);
  console.log(data.message);
  if (data.message) {
    let html = `<div>
      <div class="w-50 ms-auto">
        <div class="bg-success text-white rounded">
          <p id="chat" class="p-1">${data.message}</p>
        </div>
      </div>
    </div>`;

    $("#chat-messages").append(html);
    scrollToBottom();
  }

  if (data.user_count !== undefined) {
    console.log("user_count", data.user_count);
    document.getElementById(
      "userCount"
    ).innerHTML = `<i class="bi bi-dot text-success"></i>${data.user_count} online`;
  }
};

chatSocket.onclose = function (e) {
  console.error("Socket closed");
};
// When the send button is clicked
// collects the message in the form
document.getElementById("send").onclick = function (e) {
  // e.preventDefault() stops the server from reloading when message is sent.
  e.preventDefault();
  const messageinput = document.getElementById("message-input");
  const message = messageinput.value;

  // compiles the output as a dictionary and sends the output to consumers.py using chatSocket
  chatSocket.send(
    JSON.stringify({
      message: message,
      username: username,
      room: roomName,
    })
  );

  // resets messageinput.value to '' (empty) after sending to consumers.py
  messageinput.value = "";
};

function scrollToBottom() {
  const mcontainer = document.getElementById("chat-messages");
  mcontainer.scrollTop = mcontainer.scrollHeight;
  console.log("scroll done");
}

window.onload = function () {
  scrollToBottom();
};
