# DECISIONS.md

## 1. What is an ODM and why do we use Beanie instead of writing raw MongoDB queries?
An ODM is a tool that lets us use Python classes to work with the database
instead of writing complex MongoDB queries manually. I used Beanie because
it makes things easier and cleaner. Without it I would have to write things
like {"$set": {"field": value}} every time which is confusing especially
for a beginner like me.

## 2. What is the role of the Database class?
The Database class keeps all the database operations in one place like
save, get, update and delete. Instead of writing the same database code
in every route I just call the Database class. It made my routes much
cleaner and easier to read.

## 3. What happens if initialize_database() is not called on startup?
The app will start but when I try to use any route it will crash because
Beanie does not know which database to connect to. I noticed that without
calling it first nothing works at all.

## 4. What is the difference between Event and EventUpdate?
Event is the full document that requires all fields when creating a new
event. EventUpdate has all fields as optional so I can update just one
thing like the location without having to send all the other fields again.
Having two separate classes made the update route much simpler to work with.

## 5. Note on Pydantic version
The PDF was written using Pydantic v1 but our project uses Pydantic v2.
In v2 the BaseSettings class was moved to a separate package called
pydantic-settings. So instead of "from pydantic import BaseSettings"
I used "from pydantic_settings import BaseSettings" and installed
pydantic-settings to make it work.


 ## Part B – Docker Reflection

### 1. Why does DATABASE_URL use `mongo` as the hostname instead of `localhost`?
Because each container is isolated. When the app runs inside a container,
localhost means the container itself not my computer or the mongo container.
Docker Compose lets containers find each other by service name so I used
mongo instead. When I tried localhost the app could not connect at all.

### 2. What does depends_on do? Does it guarantee MongoDB is ready?
It makes Docker start the mongo container before the app container. But it
does not wait for MongoDB to actually be ready inside, just for the container
to start. So FastAPI might still start too early. To properly fix this you
would need a health check or retry logic.

### 3. What is the purpose of the volume in the mongo service?
It saves the database data to my local machine instead of inside the container.
Without it all my data disappears every time I run docker compose down. With
the volume the data stays in the mongo-data folder even after the container stops.

### 4. Why do we copy requirements.txt and run pip install before copying the app code?
Because Docker caches each step. If requirements.txt did not change Docker
skips the pip install on the next build and goes straight to copying the app
code. This makes rebuilding much faster. If I copied everything together it
would reinstall all packages every single time even for small code changes.