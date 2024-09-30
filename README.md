# Who's on Aux?

Who's on aux is a party game where guests get to add songs to the party playlist 
before the party starts and then guess who added each song as it plays at the party.

The point of the game is to have the most correct guesses about who added which song(s)

## About the project
Who's on Aux is a personal project that I came up with as a chance to building my full stack skills --
of course I also think it will be a fun game to play with my friends at parties!

It has a python backend built with django. At the time of writing this, the front end is HTML + Bootstrap 5.
I'm hoping use the project to learn JavaScript to make the front-end more dynamic 
once the basic structure is in place.

It also uses the spotify API to manage the playlists.

## Getting started
After cloning this repo, you'll need to add and configure some files to get started

### Set up your virtual environment

Creat a new virtual environment

```python -m venv <environment name>```

I suggest using .venv as the environment name. However, if you want to choose something else,
be sure to update the .gitignore to ignore the environment file.

activate the environment

```source <environtment name>/bin/activate```

install packages

```pip install -r requirements.txt```

### Create and configure the .env file

create the .env file

```touch .env```

open the file and add

```
DEBUG = True
SECRET_KEY =
```

Then you'll need to create a secret key.

In the terminal

```python3 manage.py shell```

In the running python shell run the following lines
```
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Take the generated code and add it to the .env file

```SECRET_KEY = <generated code>```

### Create the databases

run the following line in the terminal

```python manage.py migrate```

### Sanity check

run the following in the terminal to start the development server.

```python manage.py runserver```

And then visit [this link](http://127.0.0.1:8000/WhosOnAux/) -- it should take you to the home page