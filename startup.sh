#! /bin/bash
mkdir /tmp/mediap
cd /tmp/mediap
# install packages to build python code and provide foreign function interface - DOCKER!!!!!
sudo apt-get install python-dev build-essential autoconf libtool
wget -q \
https://raw.githubusercontent.com/onsabimana/gcloud/master/requirements.txt
wget -q \
https://raw.githubusercontent.com/onsabimana/gcloud/master/worker.py
curl https://bootstrap.pypa.io/get-pip.py | sudo python
sudo pip install virtualenv
virtualenv venv
source venv/bin/activate
venv/bin/pip install -r requirements.txt
python worker.py --subscription onsabimana_topic_subscription --dataset_id=onsabimana_media_processing --table_id=speech
