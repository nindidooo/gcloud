import time
from google.cloud import pubsub_v1 as pubsub_v1
import os

import json
import makemidi
import subprocess
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

service_account_json = 'SheetMuse-61e895319785.json'
databaseName = json.load(open(service_account_json))['databaseName']

# Fetch the service account key JSON file contents
cred = credentials.Certificate(service_account_json)

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': databaseName
})

# As an admin, the app has access to read and write all data, regradless
# of Security Rules
ref = db.reference('/root')
print(ref.get())
