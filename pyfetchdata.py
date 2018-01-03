import pyrebase

config = {
    "apiKey": "apiKey",
    "authDomain": "sheetmuse.firebaseapp.com",
    "databaseURL": "https://sheetmuse.firebaseio.com/",
    "storageBucket": "sheetmuse.appspot.com"
}

firebase = pyrebase.initialize_app(config)

# Get a reference to the auth service
auth = firebase.auth()
