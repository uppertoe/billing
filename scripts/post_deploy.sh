sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
export PATH=$PATH:/usr/local/bin
sudo chmod +x /usr/local/bin/docker-compose
sudo systemctl enable docker.service
sudo systemctl start docker.service

sudo systemctl daemon-reload
sudo systemctl enable --now backup.timer
sudo systemctl enable --now supervisord

mkdir /home/ec2-user/billing/.envs
touch /home/ec2-user/billing/.envs/.django
touch /home/ec2-user/billing/.envs/.postgres
cd /home/ec2-user/billing/.envs
echo "Now, add the .env files"
