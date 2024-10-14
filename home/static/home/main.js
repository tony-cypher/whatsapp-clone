const room = JSON.parse(document.getElementById("json-room").textContent);
if (room == "private") {
  PrivateChat();
} else if (room == "public") {
  PublicChat();
} else {
  console.log("Home. check out a message or group.");
}

function scrollToBottom() {
  const mcontainer = document.getElementById("chat-messages");
  mcontainer.scrollTop = mcontainer.scrollHeight;
}

window.onload = function () {
  scrollToBottom();
};

// --------------------------    Public chat    ---------------------//

function PublicChat() {
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
    console.log("Public chatSocket on message");
    const data = JSON.parse(e.data);
    if (data.message) {
      if (data.username == username) {
        let html = `
        <li class="common-message is-you">
        <p class="common-message-content">
          ${data.message}
        </p>
        <span class="status is-seen">✔️✔️</span>
        <time datetime>14:11</time>
      </li>`;
        $("#chat-messages .messanger-list").append(html);
      } else {
        let html = `
        <li class="common-message is-other">
        <p class="common-message-content">
          ${message.body}
        </p>
        <time datetime>14:33</time>
      </li>`;
        $("#chat-messages .messanger-list").append(html);
      }
      scrollToBottom();
    }

    if (data.user_count !== undefined) {
      console.log("user_count", data.user_count);
      document.getElementById(
        "userCount"
      ).innerHTML = `${data.user_count} online`;
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

// ----------------------    Private Chat    ------------------------//

function PrivateChat() {
  const user1_id = JSON.parse(document.getElementById("user1_id").textContent);
  const user2_id = JSON.parse(document.getElementById("user2_id").textContent);
  const chat_list = document.querySelector("#chat-messages .messanger-list");
  const username = JSON.parse(
    document.getElementById("json-username").textContent
  );

  const privateRoomName = `private_${Math.min(user1_id, user2_id)}_${Math.max(
    user1_id,
    user2_id
  )}`;
  const privateChatSocket = new WebSocket(
    "ws://" + window.location.host + "/ws/private_chat/" + privateRoomName + "/"
  );
  console.log(privateRoomName);
  privateChatSocket.onmessage = function (e) {
    console.log("privateChatSocket on message");
    const data = JSON.parse(e.data);
    if (data.message) {
      if (data.author == username) {
        let html = `
        <li class="common-message is-you">
        <p class="common-message-content">
          ${data.message}
        </p>
        <span class="status is-seen">✔️✔️</span>
        <time datetime>14:11</time>
      </li>`;
        $("#chat-messages .messanger-list").append(html);
      } else {
        let html = `
        <li class="common-message is-other">
        <p class="common-message-content">
          ${message.body}
        </p>
        <time datetime>14:33</time>
      </li>`;
        $("#chat-messages .messanger-list").append(html);
      }

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
