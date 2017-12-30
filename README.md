# RePhotoEditor

## Starting Development Server
After cloning the repo, CD into the top level directory (where manage.py is), and run the command "python manage.py runserver". 
The server will start on 127.0.0.1:8000/

## Apps
Currently, the only app is 'Website' which is located in the /website folder. This app contains the homepage, login, signup, and email verification functions.

Templates that begin with 'base_' serve as the templates that will commonly be extended upon and are not templates that will be directly rendered and served.

Website contains a new model in models.py called Profile that contains data related to email verification (User, verification code,and verification expiration date).

Website contains a custom form in forms.py that extends Django's built in signup form.  It requires the additional fields first name, last name, and email address. This form also contains the functions for email verification.

To change where the user is redirected upon login, change the setting located in settings.py.

## ToDo
1. Submit orders page
2. Setting up mail server connection (Probably just Google's SMTP server?)
    
    a. Possible our server has built in mail server capabilities? I know GoDaddy came with it.
3. Redo main content in main 'index' page
4. Change footer content
5. Change out image on 'base_logins' template
