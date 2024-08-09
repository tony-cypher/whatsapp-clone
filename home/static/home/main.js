const room = JSON.parse(document.getElementById("jroom").textContent);
if (room == "public") {
  public_group();
} else if (room == "private") {
  private_chat();
}

function public_group() {
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
    console.log("on message");
    const data = JSON.parse(e.data);
    console.log(data);
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
}

function private_chat() {
  const user1_id = JSON.parse(document.getElementById("user1_id").textContent);
  const user2_id = JSON.parse(document.getElementById("user2_id").textContent);
  const username = JSON.parse(
    document.getElementById("json-username").textContent
  );

  const privateRoomName = `private_${Math.min(user1_id, user2_id)}_${Math.max(
    user1_id,
    user2_id
  )}`;
  console.log(privateRoomName);
  const privateChatSocket = new WebSocket(
    "ws://" + window.location.host + "/ws/private_chat/" + privateRoomName + "/"
  );
  privateChatSocket.onmessage = function (e) {
    console.log("on message");
    const data = JSON.parse(e.data);
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
  };

  privateChatSocket.onclose = function (e) {
    console.error("Private chat socket closed");
  };

  document.getElementById("privateSend").onclick = function (e) {
    // e.preventDefault() stops the server from reloading when message is sent.
    e.preventDefault();
    const messageinput = document.getElementById("message-input");
    const message = messageinput.value;

    // compiles the output as a dictionary and sends the output to consumers.py using chatSocket
    privateChatSocket.send(
      JSON.stringify({
        message: message,
        author: username,
      })
    );

    // resets messageinput.value to '' (empty) after sending to consumers.py
    messageinput.value = "";
  };
}

function scrollToBottom() {
  const mcontainer = document.getElementById("chat-messages");
  mcontainer.scrollTop = mcontainer.scrollHeight;
}

window.onload = function () {
  scrollToBottom();
};
