\# OBSERVATIONS.md — Docker Lab 2



\## 1. docker run vs kubectl run



With docker run I just ran the container directly on my machine.

With kubectl run, Kubernetes handled everything. Same image but

now Kubernetes is managing it, not me directly.



\## 2. Role of the Scheduler



In the Events section of kubectl describe pod my-pod I saw

default-scheduler assigned my pod to the minikube node.

So the scheduler is what decides where the pod runs.



\## 3. Two kube-system components I recognised



\- kube-apiserver: every kubectl command goes through this,

&#x20; its the main entry point for the cluster

\- etcd: stores everything about the cluster, like a database



\## 4. postgres:16-alpine observation



The pod crashed in Task 4 because I ran it without

POSTGRES\_PASSWORD. Postgres needs that env variable to start,

without it it just fails. Once I added the env variables it

started fine. This shows that some images require specific

configuration to work and they won't start without it.



\## 5. Task 6 - why the pod didn't restart



After I deleted the pod it was just gone. Kubernetes did not

bring it back because it was a standalone pod with nothing

watching over it. To make it restart automatically I would

need a Deployment. A Deployment watches the pod and if it

goes down it creates a new one. We haven't done that yet

but thats what Lecture 4 is about.

