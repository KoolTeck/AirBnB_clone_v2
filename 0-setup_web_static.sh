#!/usr/bin/env bash
# sets up web servers for the deployment of web_static
sudo apt-get update
sudo apt-get -y install nginx
sudo mkdir -p /data/web_static/shared/ /data/web_static/releases/test
sudo chown -R ubuntu:ubuntu /data/
sudo echo  "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | tee /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R "$USER":"$USER" /etc/nginx/
sudo sed -i '21i \\tlocation \/hbnb_static {\n\t\talias /data/web_static/current;}' /etc/nginx/sites-available/default
sudo service nginx restart
