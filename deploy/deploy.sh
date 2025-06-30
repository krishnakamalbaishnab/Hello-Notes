#!/bin/bash

# HelloNotes Deployment Script
# Run this script to deploy the application

echo "🚀 Deploying HelloNotes..."

# Navigate to application directory
cd /var/www/hellonotes

# Pull latest code (if using git)
# git pull origin main

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🐍 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p static/uploads

# Set proper permissions
echo "🔐 Setting permissions..."
sudo chown -R ubuntu:ubuntu /var/www/hellonotes
chmod +x /var/www/hellonotes

# Copy systemd service file
echo "⚙️ Setting up systemd service..."
sudo cp deploy/systemd.service /etc/systemd/system/hellonotes.service
sudo systemctl daemon-reload
sudo systemctl enable hellonotes

# Copy nginx configuration
echo "🌐 Configuring nginx..."
sudo cp deploy/nginx.conf /etc/nginx/sites-available/hellonotes
sudo ln -sf /etc/nginx/sites-available/hellonotes /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test nginx configuration
sudo nginx -t

# Restart services
echo "🔄 Restarting services..."
sudo systemctl restart hellonotes
sudo systemctl restart nginx

# Check service status
echo "📊 Service status:"
sudo systemctl status hellonotes --no-pager -l
sudo systemctl status nginx --no-pager -l

echo "✅ Deployment complete!"
echo "🌐 Your application should be available at: http://your-ec2-public-ip"
echo "📋 Next steps:"
echo "1. Configure your domain DNS to point to your EC2 instance"
echo "2. Set up SSL certificate: sudo certbot --nginx -d your-domain.com"
echo "3. Update environment variables in /var/www/hellonotes/.env" 