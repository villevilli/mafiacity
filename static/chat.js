
var chat_socket = null;
var chat_lines = null;

function open_chat_socket(name) {
  chat_socket = new WebSocket("ws:"+window.location.host+"/chat_ws");
  chat_lines = document.getElementById('chat_lines');

  chat_socket.onopen = function() {
    chat_socket.send('name:'+name);
  };

  chat_socket.onmessage = function (evt) {
    var data = JSON.parse(evt.data);
    var timestamp = data["timestamp"];
    var message = data["message"];
    var p = document.createElement('p');
    p.innerHTML = timestamp + ': ' + message;
    chat_lines.appendChild(p);
  };

  chat_socket.onclose = function () {
    alert("Yhteys katkesi.");
  };
}

function send_message() {
  var chat_input = document.getElementById('chatinput');
  console.log(chat_input);
  chat_socket.send(chat_input.value);
}

