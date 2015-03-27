# StoryTeller

StoryTeller is a turn-based story writing app for Django.

## Installation

### Requirements

StoryTeller requires Python 2.7.5 with pip installed.
The app also requires a redis server. This can be obtained as follows:

##### Windows

Get the latest version of redis for Windows [here](https://github.com/rgl/redis/downloads).

##### Mac OS X and Linux

Use a package manager to install
```
redis
```

e.g.

```
brew install redis
```

```
apt-get install redis
```

### Running StoryTeller

First, install the requirements from the 'requirements.txt' file by running

```
pip install -r requirements.txt
```

---

With the requirements installed, you can now generate the database to be used by StoryTeller. To do so, run

```
python manage.py makemigrations storyteller
```

```
python manage.py migrate
```

---

With the database now created, you can run the development server. To run StoryTeller, you also need to run [SwampDragon's](http://swampdragon.net) server.py in the same folder as manage.py.
If you are using a bash terminal,a bash script (runserver.sh) has been included to allow you to run both servers in one terminal.

---

Finally, StoryTeller requires redis-server to be running to support websocket usage.

On Mac OS X and Linux simply run
```
redis-server
```

On Windows, navigate to the directory where you installed redis and run redis-server.exe from a command line.

---

The website should now be available from 127.0.0.1:8000/storyteller or localhost:8000/storyteller


## Running populate_storyteller.py

In order to run populate_storyteller.py successfully, redis-server *must* be running at the same time.
