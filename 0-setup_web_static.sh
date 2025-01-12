#!/usr/bin/env bash
# sets up web servers for the deployment of web_static
sudo apt-get update
sudo apt-get -y install nginx
mkdir -p /data/web_static/{releases/test,shared}

# Create default page
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

# Create symbolic link
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Change ownership
chown -R ubuntu /data
chgrp -R ubuntu /data

echo "Hello World!" | sudo tee /var/www/html/index.html
echo "Ceci n'est pas une page" | sudo tee /usr/share/nginx/html/404.html
printf "server {
    listen 80;
    listen [::]:80 default_server;
    root   /var/www/html/;
    index  index.html index.htm index.nginx-debian.html 404.html;

    location / {
    	add_header X-Served-By \$hostname;
    }

    location /redirect_me {
        return 301 https://google.com/;
    }

    error_page 404 /404.html;
    location /404 {
       root /usr/share/nginx/html;
       internal;
    }

    location /hbnb_static/ {
       alias /data/web_static/current/;
    }
}" > /etc/nginx/sites-available/default
sudo service nginx restart
