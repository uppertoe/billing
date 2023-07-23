sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
export PATH=$PATH:/usr/local/bin
sudo chmod +x /usr/local/bin/docker-compose
sudo systemctl enable docker.service
sudo systemctl start docker.service

sudo systemctl daemon-reload
sudo systemctl enable --now backup.timer
sudo systemctl enable --now supervisord

sudo fallocate -l 1G /swapfile
sudo chmod 600 /swapfile
sudo mkswap  /swapfile
sudo swapon /swapfile

# Append to /etc/fstab to survive reboot
line="/swapfile none swap sw 0 0"
echo "$line" | sudo tee -a /etc/fstab > /dev/null

swapon  --show
free -h

mkdir /home/ec2-user/billing/.envs
mkdir /home/ec2-user/billing/.envs/.production
touch /home/ec2-user/billing/.envs/.production/.django
touch /home/ec2-user/billing/.envs/.production/.postgres
cd /home/ec2-user/billing/.envs
echo "Now, add the .env files"
