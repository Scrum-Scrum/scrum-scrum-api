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
   - *NOTE*: To deactivate the virtual environment, type `deactivate`. However, **you should not need to do this at any time.**
7. With the 'scrum_scrum' environment active:
   - Navigate to '/vagrant/src/scrum_scrum'
     - Execute `./requirements.sh`
       - This will install the necessary python packages within the virtual environment 'scrum_scrum'

## Database Migrations
Database migrations will set up the database as it exists in its current state in the current version of the project. This applies to table/database structure, but not data in the database.
1. With the virtual environment active, navigate to '/vagrant/src/scrum_scrum/' if not already in that directory.
2. Run `python manage.py makemigrations`
3. Regardless of whether or not changes are made, it is always a good idea to execute `python manage.py migrate` after making the migrations.

## Creating your first Scrum-Scrum user
This step isn't *entirely* necessary, but you should do it so the first time you hit the user API endpoint you will actually get data back.
1. Run `python manage.py createsuperuser`
2. Follow the terminal prompts to enter the super user's information.
   - *NOTE:* Be sure to remember the password you enter, as there is currently no endpoint to update or recover a password. An easy password to use would be 'ssuCSclub1', but you can use any password you want. The createsuperuser prompt will enforce password constraints.

## Starting the development server
To test the API, you will need to tell Django to start listening for network requests.
1. Execute `python manage.py runserver 0.0.0.0:8080`
   - This tells the development server to listen for requests on any IP on port 8080.
2. You can now use the API.

## API Routes
The following API routes are currently implemented, and you can access them on the development server by replacing **_{domain}_** with **_127.0.0.1:8080_** or **_localhost:8080_** in a web browser. You don't have to access the API from a browser though; you can always interact with the API as you normally would within the client-side code by making normal API calls. In this case, your base API URL would be **_http://127.0.0.1:8080/api/_**.
### login *{domain}/api/login/*
This route returns an auth token via JSON if the supplied credentials are legitimate, or a 401 Unauthorized HTTP error if the credentials are invalid. You will need to include an Authorization header in every following HTTP request that requires a user to be "logged in". Additionally, you will need to include the client type in the HTTP request header to tell the server
which type of token you need (expiring or non-expiring). Mobile clients
receive non-expiring tokens and web clients receive expiring tokens. You should include the client header in **_every_** request, regardless of
current authenticated state or API route you are accessing. Users may authenticate with their username or email address.
- JSON: `{ "token" : "<the auth token>" }`
- Acceptable HTTP request methods:
  - POST
- Authorization header: `Authorization: Token <the auth token>`
  - *The format of the authorization header must match the above exactly*
- Client header: `client: <client_type>`
  - `<client_type>` may be *web* or *mobile*

### logout *{domain}/api/logout/*
This route revokes (deletes) the auth token that belongs to the client that initiated the logout request. This endpoint is only accessible to users who are logged in using a valid auth token. If a non-authenticated client hits this endpoint, a 401 UNAUTHORIZED error code is returned. If the request is legit, a 200 OK status is returned and the corresponding token is deleted.
- Acceptable HTTP request methods:
  - POST

### user *{domain}/api/user/*
This route allows for creation of new users or listing of all users, depending on the HTTP request method used.
- Acceptable HTTP request methods:
  - POST: create new user
  - GET: list all users

In the case of either HTTP method listed above, each will return a formatted JSON (a JSON array for GET, and a single JSON object for POST) response if it was a good request. Each individual user object will look like the following:

  {  
  &nbsp;&nbsp;"id": 1, **_(any integer corresponding to primary key)_**  
  &nbsp;&nbsp;"email": "example@scrumscrum.com",  
  &nbsp;&nbsp;"username": "scrummy",  
  &nbsp;&nbsp;"first_name": "Scrum",  
  &nbsp;&nbsp;"last_name": "Scrummy",  
  &nbsp;&nbsp;"date_joined": "2017-12-20T06:59:24.528864Z",  
  &nbsp;&nbsp;"is_active": true **_(could also be false)_**  
  }  

When you create a new user, an email template will be printed to the console. This template will include a hyperlink that must be used to activate the new account. All you need to do is copy the full link from the terminal (where the server is listening for network requests) and paste it into a new window. If the link was copy/pasted correctly, the API should return a 200 OK status code with a message about activating the account. If, for some reason, the link was corrupted or not copied properly, the API will return a 400 BAD REQUEST error code with a more detailed error message. These activation links are currently set to expire after 7 days.

**_NOTE:_** You *must* activate the new account before attempting to authenticate. It won't break anything if you don't, but you won't be able to pass auth.

### specific user *{domain}/api/user/{user_id}*
This route is essentially a detail view for a specific user corresponding to their *{user_id}* in the database.
- Acceptable HTTP request methods:
  - GET: Just list the user's information
  - PUT: Update the user's information (must be authenticated as specified user)
  - PATCH: Update the user's information (must be authenticated as specified user)
  - DELETE: Delete the user's account (must be authenticated as specified user)

### password recovery *{domain}/reset/* [Found Here](https://simpleisbetterthancomplex.com/tutorial/2016/09/19/how-to-create-password-reset-view.html)
This route is where users will go to reset their forgotten password.

You'll find in *settings.py*

`EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`

which will print the 'email' to the console.
