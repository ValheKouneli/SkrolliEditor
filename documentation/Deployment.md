Deployment
==========

These instructions are suitable for linux users.

In order to deploy this system, you need to have **python (version 3.5^)** installed in your system. You should also have **psql**, python **pip** and **git** installed.

Git clone the repository to your computer and access it.

Set up the virtual environment. If you are using unix, run command ```python3 -m venv venv```. Then artivate it by running ```source venv/bin/activate```. Now, you area ready to install all the dependencies required by the application by running command ```pip install -r requirements.txt```.

## How to set-up the database on Heroku

Install Heroku command line interface by running ```sudo snap install heroku --classic```. Then, log into Heroku by running ```heroku login```.

```cd``` into the the project repository and run ```heroku create skrollieditor```.
Then let git know about Heroku by running ```git remote add heroku```. Push everything to Heroku by running 
```
git add .
git commit -m "deployment"
git push heroku master
```
Create the database by running
```
heroku config:set HEROKU=1
heroku addons:add heroku-postgresql:hobby-dev
```

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

Now, in your project repository, connect to the heroku database by run command
```
pg:psql heroku
```
There, paste the following line:
```
INSERT INTO account (id, name, username, password, editor, admin) VALUES (1, 'Admin', 'admin', '$2b$12$0YH45mcGKYzfb1BcIQjOvextKhfbDbmRQJ2TXb2G8aM1nYxYJep5y', True, True);
```
Where the long string of random looking characters is replaced with your hashed password.

Now you can disconnect by entering ```\q```.

Now you can log in with username 'admin' and the password of your choosing.