\# Docker Lab 1 — Observations

\*\*Student:\*\* MERYEM BALILI  

\*\*Image:\*\* postgres:16-alpine



\---



\## 1. Size of the Image



The image size is 395MB. This is medium-sized because it includes the full 

PostgreSQL database engine. It is still smaller than it could be because 

it is built on Alpine Linux, which is a lightweight base image.



\---



\## 2. Image Layers



The image has about 21 layers. The largest layer (273MB) is the one that 

downloads and installs the PostgreSQL binaries. Most other layers just 

set environment variables and add 0 bytes.



\---



\## 3. Operating System and Architecture



From `docker inspect`:

\- \*\*OS:\*\* linux  

\- \*\*Architecture:\*\* amd64



\---



\## 4. Why Did the Data Disappear?



When I removed the container and created a new one, the students table 

was gone. This happened because containers do not save data permanently (stateless). 

When a container is deleted, everything inside it is deleted too.





\## 5. What Surprised Me Most



I was surprised that even though I used the same image, same database name, 

and same password, the data was completely gone after recreating the container. 



