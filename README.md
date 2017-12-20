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
Not complete yet.
