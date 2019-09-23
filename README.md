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

## Helps
I used [JWT](https://jpadilla.github.io/django-rest-framework-jwt/) for authentication so aftre calling signup API you get a token in response that should be used for the protected APIs. 
The signup and login API are unprotected but the other APIs need to send authorization token in header of HTTP request and it has bareer "JWT" in the first of token. There is an example for calling an API with token:
```sh
curl -X GET  http://127.0.0.1:8000/api/v1/flight/ -H 'Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1LCJ1c2VybmFtZSI6ImRyZmdkeWciLCJleHAiOjE1NjkzMzQzMDMsImVtYWlsIjoidGVzdEB5YWhvby5jb20iLCJpcCI6IjEyNy4wLjAuMSJ9.WLOabMLFYprawM3GfDjxGwe7Yp8sAO-MavB8ziHimcY'
```
Also for search flight API there is a sample:
```sh
curl -X GET \
  'http://127.0.0.1:8000/api/v1/flight/?flight_name=TH321&departure=Tehran&destination=Stockholm&scheduled_date=2019-10-22' \
  -H 'Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1LCJ1c2VybmFtZSI6ImRyZmdkeWciLCJleHAiOjE1NjkzMzQzMDMsImVtYWlsIjoidGVzdEB5YWhvby5jb20iLCJpcCI6IjEyNy4wLjAuMSJ9.WLOabMLFYprawM3GfDjxGwe7Yp8sAO-MavB8ziHimcY'
```

## Swagger
Also there are the list of all API with the related input in http://127.0.0.1:8000/swagger/ so you see the unprotected APIs first time but you can create a super user with below instruction:
```sh
(flightEnv)$ python manage.py createsuperuser
```
Then click on login button in Swagger page and use the credential that you set for your user. Then you see all the APIs.

## Tests

To run the tests, `cd` into the directory where `manage.py` is:
```sh
(flightEnv)$ python manage.py test authentication
(flightEnv)$ python manage.py test flight_plan
(flightEnv)$ python manage.py test users
```

