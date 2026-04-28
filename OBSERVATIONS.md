##1 A Pod is just one running container. A Deployment manages Pods and restarts them automatically if they crash. You use a Deployment because if a bare Pod dies, nothing brings it back.


##2you can change the database address in one place without touching every file. It keeps configuration separate from the app.


##3It stayed running. Two new Pods were added alongside it. Nothing was replaced.


##4 
The webapp would lose connection to the database and stop working. Kubernetes would automatically restart the MongoDB Pod, but there would be a short downtime.

