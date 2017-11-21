#! /bin/bash
mkdir /tmp/mediap
cd /tmp/mediap
sudo apt-get -y install python-dev build-essential autoconf libtool

wget -q \
https://raw.githubusercontent.com/nindidooo/gcloud/master/requirements.txt

wget -q \
https://raw.githubusercontent.com/nindidooo/gcloud/master/worker.py

wget -q \
https://raw.githubusercontent.com/nindidooo/gcloud/master/makemidi.py

curl https://bootstrap.pypa.io/get-pip.py | sudo python

sudo pip install -r requirements.txt

python worker.py --subscription onsabimana_topic_subscription --dataset_id=onsabimana_media_processing --table_id=speech
