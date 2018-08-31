Deployment
==========

These instructions are suitable for linux users.

In order to deploy this system, you need to have **python (version 3.5^)** installed in your system. You should also have **psql**, python **pip** and **git** installed.

Git clone the repository to your computer and access it.

Set up the virtual environment. If you are using unix, run command ```python3 -m venv venv```. Then artivate it by running ```source venv/bin/activate```. Now, you area ready to install all the dependencies required by the application by running command ```pip install -r requirements.txt```.

Go in the application repository and create file named ```.env``` there, and in the file, write ```ADMIN_PW="PASSWORD"``` where you replace 'PASSWORD' with a password of you choosing.

## Running the application locally

While in the virtual environment, run the application locally by running command ```python3 run.py``` on the top of the project repository.

In your browser, go to address ```localhost:5000```. Your application is running there. Now you can log in with username 'admin' and the password of your choosing.

## How to put your own version of the application online, using Heroku

[Heroku](http://www.heroku.com) is _"a cloud platform that lets companies build, deliver, monitor and scale apps"_. The code will run online. First, you have to create an account.

After creating an account, install a [heroku command line user interface](https://devcenter.heroku.com/articles/heroku-cli). Then, log into Heroku by running ```heroku login``` and give your heroku account credentials.

Decide the address you want to use for your application. It will be of the form
```
http://ADDRESSNAME.herokuapp.com
```
It's a good idea to check out first that the address you want is not in use already.

```cd``` into the the project repository and run ```heroku create ADDRESSNAME``` where you replace ADDRESSNAME with the address of your choosing.

Run ```heroku config:set ADMIN_PW="PASSWORD"``` where you replace 'PASSWORD' with a password of your choosing.

Then let git know about Heroku by running ```git remote add heroku```. Push everything to Heroku by running ```git push heroku master```.

Create the database by running
```
heroku config:set HEROKU=1
heroku addons:add heroku-postgresql:hobby-dev
```



Now you can use your browser and go to ```http://ADDRESSNAME.herokuapp.com``` and log in with username 'admin' and the password of your choosing. Change the admin password after logging in.