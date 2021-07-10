<p align="center"> <img src="https://miro.medium.com/max/2600/1*ZuM5Oa59qIP1mVIV8C-WUw.gif">

# About

My Buisness is a business management tool featuring accounts, invoices, partners, projects, and server.[Wiki](https://github.com/GDGSNF/My-Business/wiki)

# Installation

Make sure `Python >= 3.6` and `pip` are installed before proceeding with the installation instructions.

_Note: If you are following these instructions when deploying My Buisness, it is **highly** recommended that you clone the repository in `/srv`._

1. Clone this repository.

2. Create a virtual environment using `$ python3 -m venv venv`.

3. Activate the virtual environment using `$ source venv/bin/activate`.

4. Install the external `pdftk` dependency using `$ sudo apt install pdftk` for Debian based distributions.

    _Note: You may face issues installing `pdftk` on Ubuntu 18.04. Visit [this](https://askubuntu.com/questions/1028522/how-can-i-install-pdftk-in-ubuntu-18-04-and-later) link for further instructions._

5. Install the `Python` dependencies using `$ pip install -r requirements.txt`.

    _Note: You can safely ignore any errors about `bdist_wheel`._

6. Create `config.ini` by making of copy of `config.ini.defaults` using `$ cp config.ini.defaults config.ini`.

7. Edit `config.ini` with your preferred text editor and make changes to the configuration (if necessary).

    _Note:My Buisness is using a SQLite3 database while `DEBUG=True`. You don't need to specify a database user or password._

8. Apply the migrations using `$ python manage.py migrate`.

9.  Create a superuser account using `$ python manage.py createsuperuser`.

10. Enable the `Cron Jobs` using `$ python manage.py crontab add`. (You need to be logged in as the user that's running the server).

You should now have a development version of the My Buisness`accessible at`localhost:8000`or`127.0.0.1:8000`.

# Development

_Always activate the virtual environment before performing operations._

- Run the server using `$ python manage.py runserver`.

- Stop the server by pressing `Ctrl-C`.

_If you want My Buisness to send emails to the console while developing, edit `my-buisness/common/settings.py` and replace the value of `EMAIL_BACKED` with `'django.core.mail.backends.console.EmailBackend'`. Don't forget to undo this before committing!_

# Deployment

_Follow the installation instructions before continuing. If you are running the Django server, press Control-C to close it._

_Make sure you have `root` privileges._

## Django configuration

1. Collect the static files (by default in `/var/www/my-buisness/static/`) using `$ python manage.py collectstatic`.

2. Generate a `SECRET_KEY` using `$ python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`.

3. Copy the returned key to your clipboard because we will need it soon.

4. Edit `config.ini` with your preferred text editor and replace the current `SECRET_KEY` with the one you generated earlier (it's in your clipboard, right!?).

## Firewall configuration

**If you have a firewall set up (recommended), make sure to open ports 80 and 443.**

-   If you have `UFW` set up:

    -   Run `$ ufw allow http`.
    -   Run `$ ufw allow https`.

-   If don't have `UFW` and have only `iptables` set up:
    -   Open `/etc/sysconfig/iptables` for editing using your preferred text editor.
    -   Add the following lines to the file if they do not already exist, then save and exit:

```
-A INPUT -m state --state NEW -p tcp --dport 80 -j ACCEPT
-A INPUT -m state --state NEW -p tcp --dport 443 -j ACCEPT
```

## Installing additional dependencies

-   Install Gunicorn using `$ pip install gunicorn`.
-   Install Nginx using `$ apt install nginx`.
-   Install Certbot using `$ apt install python3-certbot-nginx`.

_Note: Make sure to edit the file and directory paths accordingly in the instructions below._

## Setting up the Gunicorn service

-   Edit `/etc/systemd/system/gunicorn_bt.socket` using your preferred text editor and add the following to the file:

```
[Unit]
Description=gunicorn bt socket

[Socket]
ListenStream=/run/gunicorn_bt.sock

[Install]
WantedBy=sockets.target
```

-   Edit `/etc/systemd/system/gunicorn_bt.service` using your preferred text editor and add the following to the file:

```
[Unit]
Description=gunicorn bt daemon
Requires=gunicorn_bt.socket
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/srv/my-buisness
ExecStart=/srv/business-tracer/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn_bt.sock \
          common.wsgi:application

[Install]
WantedBy=multi-user.target
```

-   Start the Gunicorn socket using `$ systemctl start gunicorn_bt.socket`.
-   Enable the Gunicorn socket (to run at startup) using `$ systemctl enable gunicorn_bt.socket`.

## Setting up Nginx

-   Remove the `default` configuration from `sites-enabled` using `$ rm /etc/nginx/sites-enabled/default`.
-   Edit `/etc/nginx/sites-available/blog` using your preferred text editor and add the following to the file:

\*Note: Make sure to replace `YOUR_FULLY_QUALIFIED_DOMAIN_NAME` with your [FQDN](https://en.wikipedia.org/wiki/Fully_qualified_domain_name).

```
server {
    listen 80;
    server_name YOUR_FULLY_QUALIFIED_DOMAIN_NAME;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        root /var/www/my-buisness;
    }

    location /media/ {
        root /var/www/my-buisness;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn_bt.sock;
    }
}
```

-   Enable the Nginx config using `$ ln -s /etc/nginx/sites-available/my-buisness /etc/nginx/sites-enabled/my-buisness`.
-   Restart Nginx using `$ systemctl restart nginx`.

## Setting up the HTTPS certificate

\*Note: Make sure to replace `YOUR_FULLY_QUALIFIED_DOMAIN_NAME` with your [FQDN](https://en.wikipedia.org/wiki/Fully_qualified_domain_name).

-   Create an HTTPS certificate with Certbot using `$ certbot --nginx -d YOUR_FULLY_QUALIFIED_DOMAIN_NAME`.
-   Follow the script instructions.
-   You should choose option 2 (Redirect) when the script asks if you want users to be redirected to the `HTTPS` version of the website if they try accessing the `HTTP` version.

Good job! You should now have a running instance of My Buisness.

# [Contributing](https://github.com/GDGSNF/My-Business/blob/master/CONTRIBUTING.md)

-   Contributions are welcome ♥.
-   Please share any features, and add unit tests! Use the pull request and issue systems to contribute.
