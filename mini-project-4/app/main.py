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
    <html>
    <body style="font-family:sans-serif;max-width:600px;margin:40px auto;padding:0 20px">
      <h2>Real-Time Polling App</h2>
      <p>Open this page in two tabs and vote — the other tab updates instantly.</p>
      <p><a href="/docs">Click here to test the REST API</a></p>
      <hr>
      <div id="poll"><p>Waiting for poll data... Make sure poll ID 1 exists.</p></div>
      <script>
        const pollId = 1;
        const ws = new WebSocket(`ws://localhost:8000/ws/polls/${pollId}`);
        ws.onmessage = (event) => {
          const poll = JSON.parse(event.data);
          let html = `<h3>${poll.question}</h3>`;
          for (const [option, count] of Object.entries(poll.options)) {
            html += `<button onclick="vote('${option}')" style="margin:6px;padding:10px 20px;font-size:15px">${option}: ${count} votes</button><br>`;
          }
          document.getElementById('poll').innerHTML = html;
        };
        ws.onerror = () => {
          document.getElementById('poll').innerHTML = '<p style="color:red">WebSocket error. Is poll 1 created?</p>';
        };
        function vote(option) {
          ws.send(JSON.stringify({ action: 'vote', option }));
        }
      </script>
    </body>
    </html>
    """