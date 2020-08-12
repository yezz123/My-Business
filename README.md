<p align="center"> <img src="https://www.mybusiness.com.au/images/my-business-logo.png">


# About
My Buisness is a business management tool featuring featuring accounts, invoices, partners, projects, and server.

# Installation

Make sure `Python >= 3.6` and `pip` are installed before proceeding with the installation instructions.

*Note: If you are following these instructions when deploying My Buisness, it is **highly** recommended that you clone the repository in `/srv`.*

1. Clone this repository.

2. Change the directory to `my-buisness` using `$ cd my-buisness/`.

3. Create a virtual environment using `$ python3 -m venv venv`.

4. Activate the virtual environment using `$ source venv/bin/activate`.

5. Install the external `pdftk` dependency using `$ apt install pdftk` for Debian based distributions.
   
   *Note: You may face issues installing `pdftk` on Ubuntu 18.04. Visit [this](https://askubuntu.com/questions/1028522/how-can-i-install-pdftk-in-ubuntu-18-04-and-later) link for further instructions.*

6. Install the `Python` dependencies using `$ pip install -r requirements.txt`.

   *Note: You can safely ignore any errors about `bdist_wheel`.*

7. Change the directory to `my-buisness` using `$ cd my-buisness/`.

8. Create `config.ini` by making of copy of `config.ini.defaults` using `$ cp config.ini.defaults config.ini`.

9. Edit `config.ini` with your preferred text editor and make changes to the configuration (if necessary).

   *Note:My Buisness is using a SQLite3 database while `DEBUG=True`. You don't need to specify a database user or password.*

8. Apply the migrations using `$ python manage.py migrate`.

9. Create a superuser account using `$ python manage.py createsuperuser`.

10. Enable the `Cron Jobs` using `$ python manage.py crontab add`. (You need to be logged in as the user that's running the server).

You should now have a development version of the My Buisness` accessible at `localhost:8000` or `127.0.0.1:8000`.

# Development

*Always activate the virtual environment before performing operations.*

- Run the server using `$ python manage.py runserver`.

- Stop the server by pressing `Ctrl-C`.

*If you want My Buisness to send emails to the console while developing, edit `my-buisness/common/settings.py` and replace the value of `EMAIL_BACKED` with `'django.core.mail.backends.console.EmailBackend'`. Don't forget to undo this before committing!*


