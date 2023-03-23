#!/bin/sh

sudo apt update
sudo apt-get upgrade -y
sudo apt autoremove
sudo apt autoclean

#Python installation
sudo apt install python3 -y
sudo apt install python3-pip -y
sudo apt install python3.10-venv -y

#uwsgi installation
sudo apt-get install uwsgi -y
sudo apt-get install uwsgi-plugin-python3 -y

#Docker installation
sudo apt-get remove docker docker.io containerd runc
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
sudo mkdir -m 0755 -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo docker run hello-world
sudo systemctl enable docker.service
sudo systemctl enable containerd.service
sudo systemctl restart docker
sudo systemctl status docker
sudo groupadd docker
sudo usermod -aG docker $USER
su - $USER
newgrp docker
id -nG
docker run hello-world

#Sysbox installation
wget https://downloads.nestybox.com/sysbox/releases/v0.5.2/sysbox-ce_0.5.2-0.linux_amd64.deb
sha256sum sysbox-ce_0.5.2-0.linux_amd64.deb
docker rm $(docker ps -a -q) -f
docker rmi $(docker images -a -q)
sudo apt-get install jq
sudo apt-get install ./sysbox-ce_0.5.2-0.linux_amd64.deb
sudo systemctl restart docker
sudo systemctl status sysbox -n20
docker info | grep -i runtime

#Portainer.io installation
docker volume create portainer_data
docker run -d -p 8000:8000 -p 9443:9443 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:latest
