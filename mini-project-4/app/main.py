import os
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import Dict, List
import json

load_dotenv()

app = FastAPI()

polls: Dict[int, dict] = {}
poll_id_counter = 1

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, poll_id: int, websocket: WebSocket):
        await websocket.accept()
        if poll_id not in self.active_connections:
            self.active_connections[poll_id] = []
        self.active_connections[poll_id].append(websocket)

    def disconnect(self, poll_id: int, websocket: WebSocket):
        if poll_id in self.active_connections:
            self.active_connections[poll_id].remove(websocket)

    async def broadcast(self, poll_id: int, message: dict):
        if poll_id in self.active_connections:
            for connection in self.active_connections[poll_id]:
                await connection.send_text(json.dumps(message))

manager = ConnectionManager()

@app.post("/polls")
def create_poll(data: dict):
    global poll_id_counter
    poll = {
        "id": poll_id_counter,
        "question": data["question"],
        "options": {option: 0 for option in data["options"]}
    }
    polls[poll_id_counter] = poll
    poll_id_counter += 1
    return poll

@app.get("/polls")
def list_polls():
    return list(polls.values())

@app.get("/polls/{poll_id}")
def get_poll(poll_id: int):
    if poll_id not in polls:
        return {"error": "Poll not found"}
    return polls[poll_id]

@app.post("/polls/{poll_id}/vote")
def vote_rest(poll_id: int, data: dict):
    if poll_id not in polls:
        return {"error": "Poll not found"}
    option = data["option"]
    if option not in polls[poll_id]["options"]:
        return {"error": "Option not found"}
    polls[poll_id]["options"][option] += 1
    return polls[poll_id]

@app.delete("/polls/{poll_id}")
def delete_poll(poll_id: int):
    if poll_id not in polls:
        return {"error": "Poll not found"}
    del polls[poll_id]
    return {"message": "Deleted"}

@app.websocket("/ws/polls/{poll_id}")
async def websocket_endpoint(websocket: WebSocket, poll_id: int):
    await manager.connect(poll_id, websocket)
    try:
        if poll_id in polls:
            await websocket.send_text(json.dumps(polls[poll_id]))
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            if message["action"] == "vote":
                option = message["option"]
                if poll_id in polls and option in polls[poll_id]["options"]:
                    polls[poll_id]["options"][option] += 1
                    await manager.broadcast(poll_id, polls[poll_id])
    except WebSocketDisconnect:
        manager.disconnect(poll_id, websocket)

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Real-Time Polling App</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #f0f2f5;
      min-height: 100vh;
      display: flex;
      align-items: flex-start;
      justify-content: center;
      padding: 48px 20px;
      color: #1a1a2e;
    }

    .container {
      background: #ffffff;
      border-radius: 20px;
      box-shadow: 0 4px 24px rgba(0,0,0,0.08), 0 1px 4px rgba(0,0,0,0.04);
      padding: 40px;
      width: 100%;
      max-width: 580px;
    }

    .header { margin-bottom: 28px; }

    .badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: #eef2ff;
      color: #4f46e5;
      font-size: 12px;
      font-weight: 600;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      padding: 4px 12px;
      border-radius: 999px;
      margin-bottom: 14px;
    }

    .badge::before {
      content: '';
      width: 7px; height: 7px;
      background: #4f46e5;
      border-radius: 50%;
      animation: pulse 1.5s infinite;
    }

    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(0.8); }
    }

    h1 {
      font-size: 26px;
      font-weight: 700;
      color: #0f0f1a;
      margin-bottom: 8px;
    }

    .subtitle {
      font-size: 14px;
      color: #6b7280;
      line-height: 1.6;
      margin-bottom: 10px;
    }

    .api-link {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      font-size: 13px;
      color: #4f46e5;
      text-decoration: none;
      font-weight: 500;
    }

    .api-link:hover { text-decoration: underline; }
    .api-link::after { content: '→'; }

    .divider {
      border: none;
      border-top: 1px solid #f0f0f5;
      margin: 24px 0;
    }

    #poll { min-height: 80px; }

    .poll-question {
      font-size: 19px;
      font-weight: 600;
      color: #0f0f1a;
      line-height: 1.4;
      margin-bottom: 20px;
    }

    .options-list {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .option-item { width: 100%; }

    .vote-btn {
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 14px 18px;
      background: #fafafa;
      border: 1.5px solid #e5e7eb;
      border-radius: 12px;
      font-size: 15px;
      font-family: inherit;
      color: #1a1a2e;
      cursor: pointer;
      transition: all 0.18s ease;
      text-align: left;
    }

    .vote-btn:hover {
      border-color: #4f46e5;
      background: #f5f3ff;
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(79,70,229,0.12);
    }

    .vote-btn:active { transform: translateY(0); box-shadow: none; }

    .option-label { font-weight: 500; }

    .vote-count {
      background: #eef2ff;
      color: #4f46e5;
      font-size: 13px;
      font-weight: 600;
      padding: 3px 11px;
      border-radius: 999px;
      white-space: nowrap;
    }

    .progress-track {
      height: 5px;
      background: #f0f0f5;
      border-radius: 999px;
      margin-top: 7px;
      overflow: hidden;
    }

    .progress-fill {
      height: 100%;
      background: linear-gradient(90deg, #6366f1, #4f46e5);
      border-radius: 999px;
      transition: width 0.5s ease;
    }

    .footer-stats {
      margin-top: 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 13px;
      color: #9ca3af;
    }

    .status-dot {
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }

    .status-dot::before {
      content: '';
      width: 7px; height: 7px;
      background: #10b981;
      border-radius: 50%;
    }

    .waiting {
      color: #9ca3af;
      font-size: 15px;
      padding: 20px 0;
    }

    .error {
      display: flex;
      align-items: center;
      gap: 10px;
      background: #fff1f2;
      border: 1px solid #fecdd3;
      border-radius: 10px;
      padding: 14px 16px;
      color: #be123c;
      font-size: 14px;
      font-weight: 500;
    }

    .error::before { content: '⚠'; font-size: 16px; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="badge">Live Poll</div>
      <h1>Real-Time Polling</h1>
      <p class="subtitle">Open this page in two tabs and vote — the other tab updates instantly.</p>
      <a class="api-link" href="/docs">Test the REST API</a>
    </div>

    <hr class="divider">

    <div id="poll">
      <p class="waiting">Waiting for poll data… make sure poll ID 1 exists.</p>
    </div>
  </div>

  <script>
    const pollId = 1;
    const ws = new WebSocket(`ws://localhost:8000/ws/polls/${pollId}`);

    ws.onmessage = (event) => {
      const poll = JSON.parse(event.data);
      const options = Object.entries(poll.options);
      const total = options.reduce((sum, [, v]) => sum + v, 0);

      let html = `<p class="poll-question">${poll.question}</p><div class="options-list">`;

      for (const [option, count] of options) {
        const pct = total > 0 ? Math.round((count / total) * 100) : 0;
        html += `
          <div class="option-item">
            <button class="vote-btn" onclick="vote('${option}')">
              <span class="option-label">${option}</span>
              <span class="vote-count">${count} vote${count !== 1 ? 's' : ''}</span>
            </button>
            <div class="progress-track">
              <div class="progress-fill" style="width: ${pct}%"></div>
            </div>
          </div>`;
      }

      html += `</div>
        <div class="footer-stats">
          <span class="status-dot">Connected</span>
          <span>${total} total vote${total !== 1 ? 's' : ''}</span>
        </div>`;

      document.getElementById('poll').innerHTML = html;
    };

    ws.onerror = () => {
      document.getElementById('poll').innerHTML =
        '<div class="error">WebSocket error. Is poll 1 created?</div>';
    };

    function vote(option) {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ action: 'vote', option }));
      }
    }
  </script>
</body>
</html>
    """