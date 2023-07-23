#!/bin/sh

cd /home/ec2-user
# Install git
sudo yum install -y git
git clone https://github.com/uppertoe/billing.git
# Will require git credentials
cd /home/ec2-user/billing/scripts
chmod +x deploy.sh
sh deploy.sh
