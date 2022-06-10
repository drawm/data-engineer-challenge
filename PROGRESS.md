> It contains a mix of detective work, ops-like work, programming and big-picture perspective

# 2022-06-07
## First look
### Readme.md
Getting a quick look around after work, I don't have much energy left so ill make it quick.

Going through the readme:
>  It contains a mix of detective work, ops-like work, programming and big-picture perspective
Interesting


ETL pipeline to store data (what about consumption?)
In -> Transform -> Out
Event -> Service -> PostgreSQL
(Versatility of events? Will fe add more in the future?)

Will need to create schema and fix/finish the prototype. Will it be worth starting over?
What is the problem the prototype is supposed to fix?


### rerun.sh & clean.sh
Should work as is

### docker-compose.yml

etl entrypoint could use env variable but it's good enough for a prototype

python services uses a prebuilt image name, will it even work?
```yml
image: data-eng-challenge/cards:latest
```
Maybe I'm missing something? Let's try it first

Yep those are available on docker.io :+1:

### Running the project
`./rerun.sh` yields an error
```log
 => ERROR [data-eng-challenge/users:latest 4/5] RUN pip install -r requirements.txt                                                    0.1s
 => CACHED [data-eng-challenge/etl:latest 3/6] COPY ./src/requirements.txt /app/requirements.txt                                       0.0s
 => ERROR [data-eng-challenge/etl:latest 4/6] RUN pip install -r requirements.txt                                                      0.1s
------
 > [data-eng-challenge/users:latest 4/5] RUN pip install -r requirements.txt:
------
------
 > [data-eng-challenge/etl:latest 4/6] RUN pip install -r requirements.txt:
------
failed to solve: executor failed running [/bin/sh -c pip install -r requirements.txt]: failed to create endpoint bcvv6u2ejq1fj04d197zkj7iq on network bridge: failed to add the host (vethef13ffd) <=> sandbox (veth7cd880c) pair interfaces: operation not supported
```
Ok I need to reboot, it's a kernel update messing up with docker network

Yet that's it, it runs now.

## Looking at the code
### users
Generate & flush random events in a loop
Files are dump in `data/events/inbox/users/`
Its simple json, always the same structure

### cards
cards can generate 3 different json structure
* new card
* modify card
* missing key (new card with a missing user_id field)

### etl
Wow, it's just an `Hello World`
Even `requirements.txt` is empty

## Recap before signing off
Ok back to the readme, it's unclear to me what should be done. What is the expected transformation?
Is it simply to move it from files to db?

:eyes:

> meant to ferry data from some services over into a Data Warehouse
> [...]
> Implement a Python-based ETL service such that events are successfully propagated from the services that
> produce events, and into the PostgreSQL database

Ok the transformation is from a json string to a table row in postgres.
This should be easy to do a "naive implementation"

I'll have to keep in mind that i'm dealing with:
* Partial/incomplete data (missing card user_id)
* Files (requiring IO operation)
    * Look into how python does async io
* Potentially large amount of data
* Un-ordered data
    * Will make card modification tricky to handle
* Can a file be overwritten while I work on it?
    * No it uses a new uuid for each file
* What do I do with events once they are stored? Move or delete?
* Don't fall into optimizing for parallel work, just keep the door open.

Even though I barely ever work with python i'm confident I can do it!


# 2022-06-10
## Getting started
Booting up my IDE, installing python plugin & looking a bit more at `etl/`
What does `wait-for-it.sh` do?
> # Use this script to test if a given TCP host/port are available
Weird, it's in a docker container, why would you need to check for available ports?

ah! It's for the database (not etl), nice!

I want to use pipenv, but I remember the readme mentioning something else, ill circle back to it once I need to install a dependency

First thing should be to do a naive approach to get to know python.
Load a file, convert json to something python can use and push it to the database
Assume best case scenario, don't think about re-parsing files or correcting incomplete json.

## Loading files
I'm going for the easiest/most straight forward way possible first
[x] Json file to Dict (json.load & open to parse)
[x] Load all events (os.scandir to use iterator and work with unknown directory size)

### What happened along the way
Here's what I did while I implemented the basic implementation
* Added helpers along the way to extract what clearly doesn't belong in the control flow
* Added an event variable to control the location of the inbox folder. It was necessary to run locally (easier for debugging) while keeping a separate config for docker
* Added volumes to `etl` service to access event files


