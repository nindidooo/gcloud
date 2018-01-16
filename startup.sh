#! /bin/bash
mkdir /tmp/mediap
cd /tmp/mediap

sudo apt-get -y install python-dev build-essential autoconf libtool

wget https://raw.githubusercontent.com/nindidooo/gcloud/master/requirements.txt

wget https://raw.githubusercontent.com/nindidooo/gcloud/master/worker2.py

wget https://raw.githubusercontent.com/nindidooo/gcloud/master/makemidi.py

curl https://bootstrap.pypa.io/get-pip.py | sudo python

sudo pip install -r requirements.txt

python worker2.py
