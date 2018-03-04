# scrum-scrum-api
API for scrum-scrum application

# Important
This branch has been created in an attempt to create the Scrum Scrum API with
[nodejs](https://nodejs.org/en/) instead of Django. For the scope of this project, Django seems to be
a little too heavy and the learning curve is _way_ too steep. As such, this is
an experimental work in progress and implementation is likely to be very fluid.

## Table of Contents
- [Prerequisites](https://github.com/Scrum-Scrum/scrum-scrum-api/tree/scrum-scrum-api-nodejs#prerequisites)
- [Getting Started](https://github.com/Scrum-Scrum/scrum-scrum-api/tree/scrum-scrum-api-nodejs#getting-started)
- [Starting the Development Server](https://github.com/Scrum-Scrum/scrum-scrum-api/tree/scrum-scrum-api-nodejs#starting-the-development-server)
- [The API](https://github.com/Scrum-Scrum/scrum-scrum-api/tree/scrum-scrum-api-nodejs#the-api)
  - [Hitting Endpoints - Basic Overview](https://github.com/Scrum-Scrum/scrum-scrum-api/tree/scrum-scrum-api-nodejs#hitting-endpoints---basic-overview)
  - [API Routes](https://github.com/Scrum-Scrum/scrum-scrum-api/tree/scrum-scrum-api-nodejs#api-routes)
    - [user](https://github.com/Scrum-Scrum/scrum-scrum-api/tree/scrum-scrum-api-nodejs#user-user)
  - [Error Responses](https://github.com/Scrum-Scrum/scrum-scrum-api/tree/scrum-scrum-api-nodejs#error-responses)


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

# The API

## Hitting Endpoints - Basic Overview
You can hit the API routes defined in the next section in a couple different
ways:

1. In a web browser on the machine hosting the Vagrant Box (VM)
2. From client-side (app) code running on the machine hosting the VM
3. From devices _other_ than the machine hosting the VM

#### Web Browser and Client-side Code - On Hosting Machine (1 & 2 above)
This is the easy part. To hit endpoints from the machine hosting your VM, just
tack the endpoint route you want to access to the end of the base API URL.

Base API URL:
```
127.0.0.1:8080/api
```
or
```
localhost:8080/api
```
whichever is easier for you.

**Example**

If you want to hit the user endpoint from the machine hosting your VM, use this
as your API URL:
```
127.0.0.1:8080/api/user
```
or
```
localhost:8080/api/user
```

#### Devices Other than the Hosting Machine
This option applies to, say, hitting an endpoint from a different computer or
a mobile app. It requires a bit of configuration, and the other device _MUST_ be
on the same network as your hosting machine (WiFi or ethernet, doesn't matter -
just has to be on the same LAN).

Follow these steps to set this up:

1. Determine your hosting machine's _internal IP address_
   - [What's my IP](https://www.whatismyip.com/) is useful. Look for "Your
   Local IP is:"
   - You can also use `ipconfig` (Windows) or `ifconfig` (UNIX-based), but these
   options are not as user-friendly
2. Once you have the local IP, open `Vagrantfile` in `scrum-scrum-api/`
3. Locate the following line:
   ```
   config.vm.network "forwarded_port", host_ip: "127.0.0.1", guest: 8080, host: 8080
   ```
4. Replace `host_ip` above with the local IP address from step 1 and save the file
5. If you have already started the VM with `vagrant up` (if not, go to step 6):
   - In the terminal of the hosting machine (_not the VM terminal after `vagrant
       ssh`!_):
      - Run `vagrant reload` from `scrum-scrum-api/`
      - Follow the steps in the `Starting the Development Server` section
6. If you have never started the VM (skip if you did step 5!):
   - Begin at [Step 3 in the `Getting Started` section](https://github.com/Scrum-Scrum/scrum-scrum-api/tree/scrum-scrum-api-nodejs#getting-started)
   and proceed through the
   [`Starting the Development Server` section](https://github.com/Scrum-Scrum/scrum-scrum-api/tree/scrum-scrum-api-nodejs#starting-the-development-server)

**Example**

Let's say you want to hit the API from a mobile application on Android or iOS.
Follow these steps (after getting the hosting and virtual machines configured
above):

1. Ensure your device is on the same LAN as your hosting machine
2. Adjust your Base API URL to use the hosting machine's local IP address instead
of `localhost` or `127.0.0.1`
3. If your hosting machine's local IP address is `10.0.0.8`, your Base API URL
will be as follows:
   ```
   10.0.0.8:8080/api
   ```

Hooray - on to routes!

## API Routes
The following API routes are currently implemented and are subject to change
during the experimental development phase.

### user: _`/user`_
This route allows for creation of new users or listing of all users, depending on the HTTP request method used.
- Acceptable HTTP request methods:
  - `POST`: create new user
  - `GET`: list all users

In the case of either HTTP method listed above, each will return a formatted JSON response if it
was a good request.

**`GET` Request Response**:

```json
{
    "user": [
        {
            "id": 1,  
            "email": "example@scrumscrum.com",
            "username": "scrummy",
            "first_name": "Scrum",
            "last_name": "Scrummy",
            "date_joined": "2017-12-20T06:59:24.528864Z",
            "is_active": true
        }
    ]
}
```

When creating a new user with a `POST` request, it is important to note that both `username` and
`email` fields are _unique_ fields in the database. All fields are `NOT NULL`,
but only the following are required and _acceptabe_ to create a user:
- email
- username
- first_name
- last_name

The other fields will be inserted automatically by the database. Attempting to
insert into or modify automatically-inserted fields will return a
`403 FORBIDDEN` error from the API.

**`POST` Request Response**:
```json
{
    "created": {
        "id": 1,  
        "email": "example@scrumscrum.com",
        "username": "scrummy",
        "first_name": "Scrum",
        "last_name": "Scrummy",
        "date_joined": "2017-12-20T06:59:24.528864Z",
        "is_active": true
    }
}
```

---

## Error Responses

Ill-formed requests or server/API problems may cause an error to be returned to
the client hitting the API. The error format is pretty basic:
```json
{
    "error": {
        "message": "Some error message or object specific to the problem"
    }
}
```
Additionally, a [W3 HTTP Protocol Status Code](https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html)
will be returned with every response regardless of whether or not an error
occurred.
