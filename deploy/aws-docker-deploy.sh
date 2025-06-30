#!/bin/bash

# HelloNotes AWS EC2 Docker Deployment Script
# Run this script on your EC2 instance

echo "🚀 Setting up HelloNotes with Docker on AWS EC2..."

# Update system packages
echo "📦 Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker
echo "🐳 Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Install Docker Compose
echo "📦 Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install nginx (for SSL termination)
echo "🌐 Installing nginx..."
sudo apt-get install -y nginx certbot python3-certbot-nginx

# Create application directory
echo "📁 Creating application directory..."
sudo mkdir -p /opt/hellonotes
sudo chown ubuntu:ubuntu /opt/hellonotes

# Create SSL directory
sudo mkdir -p /opt/hellonotes/ssl

echo "✅ Docker setup complete!"
echo "📋 Next steps:"
echo "1. Upload your code to /opt/hellonotes"
echo "2. Create .env file with your environment variables"
echo "3. Run: docker-compose -f docker-compose.prod.yml up -d"
echo "4. Set up SSL certificate with certbot" 