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
Event -> Reavice -> PostgreSQL
(Versatility of events? Will fe add more in the future?)

Will need to create schema and fix/finish the prototype. Will it be worth starting over?
What is the problem the prototype is supposed to fix?


### rerun.sh & clean.sh
Should work as is

### docker-compose.yml

etl entrypoint could use env variable but its good enough for a prototype

python sevices uses a prebuilt image name, will it even work?
```yml
image: data-eng-challenge/cards:latest
```
Maybe i'm missing something, lets try it first
yep those are available on docker.io :+1:

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
Ok I need to reboot, its a kernel update messing up with docker network

Yet thats it, it runs now.

## Looking at the code
### users
Generate & flush random events in a loop
Files are dump in `data/events/inbox/users/`
Its simple json, always the same structure

### cards
cards can generate 3 different json structure
* new card
* modify card
* missing key (new card witha  missing user_id field)

### etl
Wow its just an `Hello World`
Even `requirements.txt` is empty

## Recap before signing off
Ok back to the readme, its unclear to me what should be done. What is the expected transformation?
Is it simply to move it from files to db?

:eyes:

> meant to ferry data from some services over into a Data Warehouse
> [...]
> Implement a Python-based ETL service such that events are successfully propagated from the services that
> produce events, and into the PostgreSQL database

Ok the tansformation is from a json string to a table row in postgres.
This should be easy to do a "naive implementation"

Ill have to keep in mind that i'm dealing with:
* Partial/incomplete data (missing card user_id)
* Files (requiring IO operation)
    * Look into how python does async io
* Potentially large amount of data
* Un-ordered data
    * Will make card modification tricky to handle
* Can a file be overitten while I work on it?
    * No it uses a new uuid for each file
* What do I do with events once they are stored? Move or delete?
* Don't fall into optimizing for parallel work, just keep the door open.



Even though I barely ever work with python i'm confident I can do it!
