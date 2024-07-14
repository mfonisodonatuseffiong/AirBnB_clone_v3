#!/usr/bin/env bash
# Bash script that sets up web servers for the deployment of web_static

# Update package lists and install Nginx if it's not already installed
sudo apt-get update
sudo apt-get -y install nginx

# Allow 'Nginx HTTP' through the firewall
sudo ufw allow 'Nginx HTTP'

# Create the necessary directories if they don't already exist
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a simple HTML file
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Remove the existing symbolic link if it exists
sudo rm -f /data/web_static/current

# Create a new symbolic link
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the directories to the ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Check if the location block already exists and remove it to avoid duplication
if grep -q 'location /hbnb_static {' /etc/nginx/sites-enabled/default; then
    echo "Removing existing location block..."
    sudo sed -i '/location \/hbnb_static {/,+2 d' /etc/nginx/sites-enabled/default
fi

# Add the location block at the end of the server block
echo "Adding new location block..."
sudo sed -i '/server {/a \\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-enabled/default

# Test the Nginx configuration for syntax errors
if sudo nginx -t; then
    echo "Nginx configuration is successful. Restarting Nginx..."
    sudo service nginx restart
else
    echo "Nginx configuration test failed."
    exit 1
fi

echo "Setup complete."
