(function () {
  const API = "http://127.0.0.1:8000"; // change later to deployed backend

  let sessionId = null;

  // ---- Create UI ----
  const toggle = document.createElement("div");
  toggle.innerHTML = "💬";
  toggle.style = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: #2e7d32;
    color: white;
    width: 55px;
    height: 55px;
    border-radius: 50%;
    display:flex;
    align-items:center;
    justify-content:center;
    cursor:pointer;
    z-index:9999;
  `;

  const box = document.createElement("div");
  box.style = `
    position: fixed;
    bottom: 90px;
    right: 20px;
    width: 320px;
    background: #111;
    color: white;
    border-radius: 10px;
    padding: 10px;
    display:none;
    z-index:9999;
  `;

  const messages = document.createElement("div");
  messages.style = "max-height:250px;overflow-y:auto;";

  const options = document.createElement("div");

  const input = document.createElement("input");
  input.placeholder = "Type...";
  input.style = "width:70%;padding:5px;";

  const send = document.createElement("button");
  send.innerText = "Send";

  box.appendChild(messages);
  box.appendChild(options);
  box.appendChild(input);
  box.appendChild(send);

  document.body.appendChild(toggle);
  document.body.appendChild(box);

  // ---- Toggle ----
  toggle.onclick = () => {
    box.style.display = box.style.display === "none" ? "block" : "none";
  };

  // ---- Helpers ----
  function addMessage(text, sender) {
    const div = document.createElement("div");
    div.innerText = text;
    div.style = `
      margin:5px;
      padding:6px;
      border-radius:6px;
      background:${sender === "user" ? "#4CAF50" : "#333"};
      text-align:${sender === "user" ? "right" : "left"};
    `;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  }

  function renderOptions(opts) {
    options.innerHTML = "";
    opts.forEach(o => {
      const btn = document.createElement("button");
      btn.innerText = o;
      btn.onclick = () => sendAnswer(o);
      options.appendChild(btn);
    });
  }

  async function startChat() {
    const res = await fetch(API + "/start", { method: "POST" });
    const data = await res.json();

    sessionId = data.sessionId;
    addMessage(data.message, "bot");
    renderOptions(data.options);
  }

  async function sendAnswer(answer) {
    addMessage(answer, "user");

    const res = await fetch(API + "/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sessionId, answer })
    });

    const data = await res.json();

    addMessage(data.message, "bot");
    renderOptions(data.options || []);
  }

  send.onclick = () => {
    const val = input.value;
    if (!val) return;
    input.value = "";
    sendAnswer(val);
  };

  startChat();
})();