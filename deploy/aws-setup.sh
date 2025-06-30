#!/bin/bash

# HelloNotes AWS EC2 Setup Script
# Run this script on your EC2 instance after connecting via SSH

echo "🚀 Setting up HelloNotes on AWS EC2..."

# Update system packages
echo "📦 Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install Python and pip
echo "🐍 Installing Python and pip..."
sudo apt-get install -y python3 python3-pip python3-venv

# Install nginx
echo "🌐 Installing nginx..."
sudo apt-get install -y nginx

# Install MongoDB (if you want to self-host)
# echo "🍃 Installing MongoDB..."
# wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
# echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
# sudo apt-get update
# sudo apt-get install -y mongodb-org
# sudo systemctl start mongod
# sudo systemctl enable mongod

# Install additional dependencies
echo "🔧 Installing additional dependencies..."
sudo apt-get install -y curl git build-essential

# Create application directory
echo "📁 Creating application directory..."
sudo mkdir -p /var/www/hellonotes
sudo chown ubuntu:ubuntu /var/www/hellonotes

# Install certbot for SSL
echo "🔒 Installing SSL certificate tools..."
sudo apt-get install -y certbot python3-certbot-nginx

echo "✅ Basic system setup complete!"
echo "📋 Next steps:"
echo "1. Upload your code to /var/www/hellonotes"
echo "2. Set up your environment variables"
echo "3. Configure nginx"
echo "4. Set up SSL certificate" 