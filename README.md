# scrum-scrum-api
API for scrum-scrum application

# Important
This branch has been created in an attempt to create the Scrum Scrum API with
[nodejs](https://nodejs.org/en/) instead of Django. For the scope of this project, Django seems to be
a little too heavy and the learning curve is _way_ too steep. As such, this is
an experimental work in progress and implementation is likely to be very fluid.

## Prerequisites
In order to use this API during development, a few pieces of software are required.
- [VirtualBox](https://www.virtualbox.org/)
  - Used for virtual dev server
- [Vagrant](https://www.vagrantup.com/)
  - Used to download and configure the dev server image
- UNIX Terminal or [Git Bash (Windows)](https://git-scm.com/downloads)

## Getting Started
1. Clone the project so you have a local copy.
2. Open the terminal or git bash (Windows)
3. Navigate to the top-level directory of scrum-scrum-api/
4. Run `npm install`
   - This will probably take a minute or two
4. Type `vagrant up` into the command line
   - This will likely take a few minutes the first time the image is installed
5. Once `vagrant up` completes, type `vagrant ssh`
   - This will connect you to the dev server

Your dev server is ready!

## Starting the Development Server
To test the API, you will need to start the dev server so it listens for
incoming requests on **localhost:8080** (**127.0.0.1:8080**). There is more info
on how to hit specific routes below.

**_NOTE_**: Step 2 is critical!

Follow these steps to start the server:
1. _After_ running `vagrant ssh` above, navigate to `/vagrant`
   - If you run `pwd`, you should see `/vagrant` output to the console
2. Run the applicable npm script below
   - _If you have never started the dev server, or you've deleted the Vagrant Box_:
      - Run `npm run first`
   - _If you have started the dev server before without deleting the Vagrant Box_:
      - Run `npm start`
3. You should see `[nodemon] starting 'node <some-file-name>'`
   - `<some-file-name>` will be the filename of the entry point (could change
       during development)
4. You can now hit API routes!

---

## API Routes
The following API routes are currently implemented, and you can access them on the development server by replacing **_{domain}_** with **_127.0.0.1:8080_** or **_localhost:8080_** in a web browser.

For development, your base API URL would be **_http://127.0.0.1:8080/api/_**.

**_NOTE_**: I haven't tested hitting the API from outside a browser _on the
machine running the dev server_. Unfortunately this means mobile app developers
may have to figure out some way to do this in the meantime until I have time to
figure it out.

### user: _{domain}/api/user/_
This route allows for creation of new users or listing of all users, depending on the HTTP request method used.
- Acceptable HTTP request methods:
  - `POST`: create new user
  - `GET`: list all users

In the case of either HTTP method listed above, each will return a formatted JSON (a JSON array for GET, and a single JSON object for POST) response if it was a good request. Each individual user object will have the same structure as the
following:

  {  
  &nbsp;&nbsp;"id": 1, **_(any integer corresponding to primary key)_**  
  &nbsp;&nbsp;"email": "example@scrumscrum.com",  
  &nbsp;&nbsp;"username": "scrummy",  
  &nbsp;&nbsp;"first_name": "Scrum",  
  &nbsp;&nbsp;"last_name": "Scrummy",  
  &nbsp;&nbsp;"date_joined": "2017-12-20T06:59:24.528864Z",  
  &nbsp;&nbsp;"is_active": true **_(could also be false)_**  
  }

When creating a new user, it is important to note that both `username` and
`email` fields are _unique_ fields in the database. All fields are `NOT NULL`,
but only the following are required to create a user:
- email
- username
- first_name
- last_name

The other fields will be inserted automatically by the database.
