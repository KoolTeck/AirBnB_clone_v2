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
# Create default page
echo "Holberton School" > /var/www/html/index.html

# Configurate server
ufw allow 'Nginx HTTP'

f_config="/etc/nginx/sites-available/default"
# Add redirection
new_site="https://github.com/EstephaniaCalvoC/"
sed -i "/listen 80 default_server/a rewrite ^/redirect_me $new_site permanent;" $f_config

# Add 404 redirection
echo "Ceci n'est pas une page" > /usr/share/nginx/html/my_404.html
new_404="my_404.html"
l_new_404="/my_404.html {root /usr/share/nginx/html;\n internal;}"
sed -i "/listen 80 default_server/a error_page 404 /$new_404; location = $l_new_404" $f_config
sed -i '/listen 80 default_server/a location /hbnb_static/ { alias /data/web_static/current/;}' $f_config

sudo service nginx restart
