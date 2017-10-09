Provisioning a new site
=======================

## Required packages:

* nginx
* Python 3.6
* virtualenv + pip
* Git

eg, on Ubuntu:

    sudo add-apt-repository ppa:fkrull/deadsnakes
    sudo apt-get install nginx git python36 python3.6-venv

## Nginx Virtual Host config

* see nginx.template.conf
* replace SITENAME with, e.g., staging.my-domain.com

## Systemd service

* see gunicorn-systemd.template.service
* replace SITENAME with, e.g., staging.my-domain.com

## Folder structure:
Assume we have a user account at /home/username

/home/username
└── sites
    └── SITENAME
         ├── database
         ├── source
         ├── static
         └── virtualenv


## PERMISSIONS
nginx and gunicorn services are configured to run from a limited permission
user account, www-data. Ensure that relevant directories (e.g. database) are
updated accordingly.
Recommended: sudo chmod 755 database
Recommended: sudo chown -R www-data:www-data database

## STEPS TO COMPLETE
1. Ensure latest changes pushed to remote repository (e.g. github)

2. Run the fabfile
        cd deploy_tools && fab deploy:host=user@site_url

3. ssh into your server and cd to sites/site_url_goes_here/source

4. Create nginx virtual host using the provided templates
   (HINT: sed s/replaceme/withthis/g)
        sed "s/SITENAME/site_url_goes_here/g" \
        deploy_tools/nginx.template.conf \
        | sudo tee /etc/nginx/sites-available/site_url_goes_here

5. Activate symlink
        sudo ln -s ../sites-available/site_url_goes_here \
        /etc/nginx/sites-enabled/site_url_goes_here

6. Write the systemd service
        sed "s/SITENAME/site_url_goes_here/g" \
        deploy_tools/gunicorn-systemd.template.service \
        | sudo tee /etc/systemd/system/gunicorn-site_url_goes_here.service

7. Start up the relevant services
        sudo systemctl daemon-reload
        sudo systemctl reload nginx
        sudo systemctl enable gunicorn-superlists.ottg.eu
        sudo systemctl start gunicorn-superlists.ottg.eu

8. Visit your URL in the browser
