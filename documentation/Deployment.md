Deployment
==========

These instructions are suitable for linux users.

In order to deploy this system, you need to have **python (version 3.5^)** installed in your system. You should also have **psql**, python **pip** and **git** installed.

Git clone the repository to your computer and access it.

Set up the virtual environment. If you are using unix, run command ```python3 -m venv venv```. Then artivate it by running ```source venv/bin/activate```. Now, you area ready to install all the dependencies required by the application by running command ```pip install -r requirements.txt```.

## Running the application locally

While in the virtual environment, run the application locally by running command ```python3 run.py``` on the top of the project repository. This initiates the database. Press ```Ctrl + C``` the stop the application.

Now, you want to create an admin account to your local database. Follow the instructions on **"Hashing password"** and come back here.

If you don't have **sqlite3** installed, install it. Access the database by running command ```sqlite3 application/database.db``` on the top of the repository. Insert line 

```
INSERT INTO account (id, name, username, password, editor, admin) VALUES (1, 'Admin', 'admin', '$2b$12$0YH45mcGKYzfb1BcIQjOvextKhfbDbmRQJ2TXb2G8aM1nYxYJep5y', 1, 1);
```
where the long string of random looking characters is replaced with your hashed password.

Now you can disconnect by entering ```.exit```.

Start the application again by running command ```python3 run.py```. In your browser, go to address ```localhost:5000```. Your application is running there.

Now you can log in with username 'admin' and the password of your choosing.

## How to put your own version of the application online, using Heroku

[Heroku](http://www.heroku.com) is _"a cloud platform that lets companies build, deliver, monitor and scale apps"_. The code will run online. First, you have to create an account.

After creating an account, install a [heroku command line user interface](https://devcenter.heroku.com/articles/heroku-cli). Then, log into Heroku by running ```heroku login``` and give your heroku account credentials.

Decide the address you want to use for your application. It will be of the form
```
http://ADDRESSNAME.herokuapp.com
```
It's a good idea to check out first that the address you want is not in use already.

```cd``` into the the project repository and run ```heroku create ADDRESSNAME``` where you replace ADDRESSNAME with the address of your choosing.

Then let git know about Heroku by running ```git remote add heroku```. Push everything to Heroku by running ```git push heroku master```.

Create the database by running
```
heroku config:set HEROKU=1
heroku addons:add heroku-postgresql:hobby-dev
```

Follow the instruction on **"Hashing password"** an come back to here.

Now, in your project repository, connect to the heroku database by run command
```
heroku pg:psql
```
There, paste the following line:
```
INSERT INTO account (id, name, username, password, editor, admin) VALUES (1, 'Admin', 'admin', '$2b$12$0YH45mcGKYzfb1BcIQjOvextKhfbDbmRQJ2TXb2G8aM1nYxYJep5y', True, True);
```
where the long string of random looking characters is replaced with your hashed password.

Now you can disconnect by entering ```\q```.

Now you can log in with username 'admin' and the password of your choosing.

## Hashing password

To create an admin account, you have to choose a password and hash it.
To do this, open an interactive python interpreter by running ```python3```.
Then in the interactive python interpreter, run ```import bcrypt``` and
```
bcrypt.hashpw('MYPASSWORD'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
```
where you replace MYPASSWORD with a password of your choosing.
Copy the string of characters that follows, which is the hashed password. It should be of the format
```$2b$12$0YH45mcGKYzfb1BcIQjOvextKhfbDbmRQJ2TXb2G8aM1nYxYJep5y```

Close the interactive python interpreter by running ```exit()```.