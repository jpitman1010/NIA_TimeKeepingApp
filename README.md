# NIA_TimeKeepingApp

## Tech Stack:

-Flask (backend web framework)

- Python (backend web framework)
- SQL Alchemy (interface for back to front end)
- PSQalchemy
- Javascript (canvas)
- Jinja (sessions)
- JQuery and AJAX (form handling)
- CSS (front-end)

# API's Used:

- Cloudinary API

# What the web app can do:

1. Registration of New user.
   a. First & Last Name, Photo, email, password.
2. Log In
3. Clock In, Clock Out simple button page for quick access to time punches.
4. Calendar page to view previous time punches, request PTO (which is approved or denied from admin user), view schedule, set schedule, request time punch change for mistaken or missing time punch (which will pend verification from admin).
5. Sick Pay -keep track of balances as time is used.
6. Holiday Pay- keep track of balances as time is used.
7. Admin
   a. View all time punches
   b. Approve/Deny and give comments for missing time punches, PTO (may save limits for different types of employees), holiday pay (may set limits depending on local holidays and legal requirements),

### Installation and Start Up

Timekeeping App requires [Node.js](https://nodejs.org/) v4+ to run.

Install the dependencies and devDependencies and start the server.

```sh
$ cd timekeepingNotReact
$ npm install -d
$ node app

# start your virtual environment
$ pip install virtualenv

# check environment version:
$ virtualenv --version

#First, let us create a folder .virtualenvs in the home directory. This is where we will keep all our virtual environments.
$ cd ~
$ mkdir .virtualenvs
$ cd .virtualenvs


#From inside the .virtualenvs directory, create a new virtual environment using virtualenv
$ virtualenv venv

#Now, let us activate the virtual environment
$ source venv/bin/activate

#Future logging into venv in one line:
$ cd ~/.virtualenvs/
$ source venv/bin/activate
$ cd ~/Desktop/timekeepingApp/NIA_TimeKeepingApp


# cloudinary use:
$ source secrets.sh

#Create the PostgreSQL database:


#Mac Users:
$ initdb timekeeperNIA
#>>>Success. You can now start the database server using:
$ pg_ctl -D timekeeperNIA -l logfile start
#Mac- if unable to get postgres to start because port in use, check and kill:
$ lsof -i:5432
$ kill -15 (PID)
#Linnux- if unable to get postgres to start becaus port in use check and kill:
$ ps -ef | grep postgres
$ sudo pkill -u postgres
   #if still having problems starting postgres you can use:
   $ sudo service postgresql initdb
   $ sudo systemctl enable postgresql
   $ sudo systemctl start postgresql
   $ sudo ps -ef | grep postgres

#Linnux creating tables from model.py
$ python3 -i model.py
$ db.create_all()
#>>>output should show tables from model.py


#can check database by going through umbuntu or VS code- type in psql timekeeperNIA
#to get into database, then type \dt to pull up list of tables created...then \d tablename
#to get table attributes, then SELECT * from  (tablename) to see everything on table.

#drop database linnux:
$ sudo -u postgres dropdb (dbname)

#drop database Mac:
$ dropdb (dbname)

#Both Systems
$ pip3 install -r requirements.txt
# add API key for Cloudinary to a secrets.sh file, be sure to git-ignore the file to keep the API secret
$ source secrets.sh
$ npm install bootstrap
$ python3 model.py
$ python3 server.py
```

[//]: # "These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax"
[//]: # "**Free Software, Hell Yeah!**"
[git-repo-url]: https://github.com/jpitman1010/project3.0.git
[jquery]: http://jquery.com
