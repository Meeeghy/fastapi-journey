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