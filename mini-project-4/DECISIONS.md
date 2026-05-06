\# DECISIONS.md



\## 1. Connection Management

I used a class called ConnectionManager that has a dictionary to keep track

of who is connected. The key is the poll ID and the value is a list of

websocket connections. When someone closes the tab, the WebSocketDisconnect

error is caught and I remove them from the list. The app does not crash.



\## 2. State Storage

I saved the votes in a normal Python dictionary because it was simple and

the project did not need a database. The problem is if I restart the server

everything is gone. If this was a real app I would use a database like

PostgreSQL so the data stays saved.



\## 3. Concurrency

I did not handle this fully. If two people vote at the exact same time the

count might be wrong because both could read the same number before either

one updates it. For a real app I would need to use a database with atomic

operations to fix this.



\## 4. REST vs WebSocket

With POST /polls/{id}/vote only the server gets updated. Other people

watching the poll in their browser will not see the change unless they

refresh. With WebSocket when someone votes everyone connected sees the

update immediately without refreshing. REST is just a backup option.

