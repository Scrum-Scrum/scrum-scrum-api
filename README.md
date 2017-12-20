# scrum-scrum-api
API for scrum-scrum application

## Prerequisites
In order to use this API, a few pieces of software are required.
- VirtualBox https://www.virtualbox.org/
  - Used for virtual dev server
- Vagrant https://www.vagrantup.com/
  - Used to download and configure the dev server image
- UNIX Terminal or Git Bash (Windows) https://git-scm.com/downloads

## Getting Started
1. Clone the project so you have a local copy.
2. Open the terminal or git bash (Windows)
3. Navigate to the top-level directory of scrum-scrum-api/
4. Type `vagrant up` into the command line
   - This will likely take a few minutes the first time the image is installed
5. Once `vagrant up` completes, type `vagrant ssh`
   - This will connect you to the dev server
   - Some additional setup will occur automatically
6. Once connected to the dev server and all additional setup is complete, type `workon scrum_scrum`
   - This activates the virtual environment in which the API project will execute
     - You will see '(scrum_scrum)' at the beginning of the command-line prompt if this part is successful
       - If you already see '(scrum_scrum)' at the beginning of the command-line prompt, proceed to step 7 (you can still execute `workon scrum_scrum`, but nothing will happen).
     - **Make sure to always work within the virtual environment 'scrum_scrum' while interacting with the project.**
   - *NOTE*: To deactivate the virtual environment, type `deactivate`
7. With the 'scrum_scrum' environment active:
   - Navigate to '/vagrant/src/scrum_scrum'
     - Execute `./requirements.sh`
       - This will install the necessary python packages within the virtual environment 'scrum_scrum'

## Database Migrations
Database migrations will set up the database as it exists in its current state in the current version of the project.
1. With the virtual environment active, navigate to '/vagrant/src/scrum_scrum/' if not already in that directory.
2. Run `python manage.py makemigrations`
3. Regardless of whether or not changes are made, it is always a good idea to execute `python manage.py migrate` after making the migrations.

## Starting the development server
To test the API, you will need to tell Django to start listening for network requests.
1. Execute `python manage.py runserver 0.0.0.0:8080`
   - This tells the development server to listen for requests on any IP on port 8080.
2. You can now use the API.

## API Routes
The following API routes are currently implemented, and you can access them on the development server by replacing *<domain>* with *127.0.0.1:8080* or *localhost:8080* in a web browser.
### login *<domain>/api/login/*
This route returns an auth token via JSON if the supplied credentials are legitimate, or a 400 BAD REQUEST HTTP error if the credentials are invalid. You will need to include an Authorization header in every following HTTP request that requires a user to be "logged in".
- JSON: `{ "token" : "<the auth token>" }`
- Acceptable HTTP request methods:
  - POST
- Authorization header: `Authorization: Token <the auth token>`
  - *The format of the authorization header must match the above exactly*
### user *<domain>/api/user/*
This route allows for creation of new users or listing of all users, depending on the HTTP request method used.
- Acceptable HTTP request methods:
  - POST: create new user
  - GET: list all users

In the case of either HTTP method listed above, each will return a formatted JSON (a JSON array for GET, and a single JSON object for POST) response if it was a good request. Each individual user object will look like the following:

  {
    "id": 1, **_(any integer corresponding to primary key)_**
    "email": "example@scrumscrum.com",
    "username": "scrummy",
    "first_name": "Scrum",
    "last_name": "Scrummy",
    "date_joined": "2017-12-20T06:59:24.528864Z",
    "is_active": true **_(could also be false)_**
  }

### specific user *<domain>/api/user/<user_id>*
This route is essentially a detail view for a specific user corresponding to their *<user_id>* in the database.
- Acceptable HTTP request methods:
  - GET: Just list the user's information
  - PUT: Update the user's information (must be authenticated as specified user)
  - PATCH: Update the user's information (must be authenticated as specified user)
  - DELETE: Delete the user's account (must be authenticated as specified user)
