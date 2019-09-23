#  Flight application

## Setup

Create a virtual environment (with python 3) to install dependencies in and activate it:

### Install **pip** first

    sudo apt-get install python3-pip

### Then install **virtualenv** using pip3

    sudo pip3 install virtualenv 

### Now create a virtual environment 

    virtualenv flightEnv 

### Active your virtual environment:    
    
    source flightEnv/bin/activate

The second thing to do is to clone the repository:

```sh
$ git clone https://github.com/mrezaei1367/flight.git

```

Then install the dependencies:

```sh
(flightEnv)$ cd flight
(flightEnv)$ pip install -r requirements.txt
```
Note the `(flightEnv)` in front of the prompt.

Once `pip` has finished downloading the dependencies:
```sh
(flightEnv)$ python manage.py makemigrations
(flightEnv)$ python manage.py migrate
(flightEnv)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`.


## Tests

To run the tests, `cd` into the directory where `manage.py` is:
```sh
(flightEnv)$ python manage.py test authentication
(flightEnv)$ python manage.py test flight_plan
(flightEnv)$ python manage.py test users
```

