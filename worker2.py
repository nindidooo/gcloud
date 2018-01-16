
#!/usr/bin/env python

# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This application demonstrates how to perform basic operations on
subscriptions with the Cloud Pub/Sub API.
For more information, see the README.md under /pubsub and the documentation
at https://cloud.google.com/pubsub/docs
"""
import time
import json
import makemidi
import subprocess
import os
from firebase import firebase
import importaudio

import os
import platform


def list_subscriptions_in_topic(project, topic_name):
    """Lists all subscriptions for a given topic."""
    subscriber = pubsub_v1.SubscriberClient()
    topic_path = subscriber.topic_path(project, topic_name)

    for subscription in subscriber.list_subscriptions(topic_path):
        print(subscription.name)


def list_subscriptions_in_project(project):
    """Lists all subscriptions in the current project."""
    subscriber = pubsub_v1.SubscriberClient()
    project_path = subscriber.project_path(project)

    for subscription in subscriber.list_subscriptions(project_path):
        print(subscription.name)


def create_subscription(project, topic_name, subscription_name):
    """Create a new pull subscription on the given topic."""
    subscriber = pubsub_v1.SubscriberClient()
    topic_path = subscriber.topic_path(project, topic_name)
    subscription_path = subscriber.subscription_path(
        project, subscription_name)

    subscription = subscriber.create_subscription(
        subscription_path, topic_path)

    print('Subscription created: {}'.format(subscription))


def delete_subscription(project, subscription_name):
    """Deletes an existing Pub/Sub topic."""
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(
        project, subscription_name)

    subscriber.delete_subscription(subscription_path)

    print('Subscription deleted: {}'.format(subscription_path))


def receive_messages(project, subscription_name):
    """Receives messages from a pull subscription."""
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(
        project, subscription_name)

    def callback(message):

        attributes = message.attributes
        event_type = attributes['eventType']

        bucket_id = attributes['bucketId']
        object_id = attributes['objectId']

        if event_type == 'OBJECT_DELETE':

            print('\n ######################## ' + object_id +
                  ' DELETED FROM STORAGE ########################')

            # print('\ninside function: receive_messages\n')
            # print('Received message: {}'.format(message))
            # print('MATT Received message: {}'.format(message.data))

        if event_type == 'OBJECT_FINALIZE':

            print('\n ######################## ' + object_id +
                  ' UPLOADED TO STORAGE ########################')

            data = message.data
            msg_data = json.loads(data)
            mediaLink = msg_data["mediaLink"]

            print('\nreceived file: ', mediaLink)

            print('bucket_id', bucket_id)
            print('object_id', object_id)

            if '.3gp' in object_id or '.aac' in object_id or '.adts' in object_id or '.mp3' in object_id or '.mp4' in object_id:

                # os.system('rm -f *.mid')
                # os.system('rm -f *.aac')

                print('downloading object...')

                file = ' gs://' + bucket_id + '/' + object_id

                download = 'gsutil cp ' + file + ' .'

                os.system(download)

                # file has been downloaded to vitrual agent

                # now get metadata of the file

                # print('getting metadata...')
                # getmetadata = 'gsutil ls -L ' + file
                # os.system(getmetadata)

                # now get hash of the file
                # gethash = 'gsutil hash -m ' + file
                # # os.system(gethash)

                # md5Hash = os.popen(gethash).read()[75:99]
                # midi_filename = md5Hash + '.mid'  # "major-scale.mid"

                #### HERE IS WHERE ALGORITHM GOES #####
                print 'object_id', object_id

                audioFile = importaudio.processAudio(object_id)
                # audioFile.printFileName()
                # audioFile.playaudio()

                # create midi file
                audio_filename = object_id[0:19]

                midi_filename = audio_filename + '.mid'

                makemidi.create_midi(midi_filename)

                #######################################

                # On completion, remove input audio file from storage...
                # remove = 'gsutil rm gs://' + bucket_id + '/' + object_id
                # os.system(remove)

                print('\nuploading midi...')
                set_midi_metadata = 'gsutil setmeta -h x-goog-meta-userID:MATTHEW' + \
                    ' gs://' + bucket_id + '/' + midi_filename
                upload_midi = 'gsutil cp ' + midi_filename + ' gs://' + bucket_id
                os.system(upload_midi)
                # os.system(set_midi_metadata)

                print('updating database')
                result = firebase.get(audio_filename, 'mididownload')
                resultPut = firebase.put(
                    audio_filename, 'midifile', midi_filename)
                print('result = ', result)
                print('resultPut = ', resultPut)

        message.ack()
        # time.sleep(2)
        print('\ncleaning out files:')  # , midi_filename, ' and ', object_id
        os.system('rm -f *.mid')  # , midi_filename)
        os.system('rm -f *.aac')  # , object_id)
        os.system('rm -f *.mp4')  # , object_id)
        # time.sleep(7)
        print('\n\nDONE')

    subscriber.subscribe(subscription_path, callback=callback)

    # The subscriber is non-blocking, so we must keep the main thread from
    # exiting to allow it to process messages in the background.
    print('Listening for messages on {}'.format(subscription_path))
    while True:
        time.sleep(1)


def receive_messages_with_flow_control(project, subscription_name):
    """Receives messages from a pull subscription with flow control."""
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(
        project, subscription_name)

    def callback(message):
        print('\ninside function: receive_messages_with_flow_control\n')
        print('Received message: {}'.format(message))
        print('MATT Received message: {}'.format(message.data))
        message.ack()

    # Limit the subscriber to only have ten outstanding messages at a time.
    flow_control = pubsub_v1.types.FlowControl(max_messages=10)
    subscriber.subscribe(
        subscription_path, callback=callback, flow_control=flow_control)

    # The subscriber is non-blocking, so we must keep the main thread from
    # exiting to allow it to process messages in the background.
    print('Listening for messages on {}'.format(subscription_path))
    while True:
        time.sleep(60)


if __name__ == '__main__':

    op_system = platform.system()
    print 'Environment detected:', op_system

    if op_system == 'Linux':
        from google.cloud import pubsub as pubsub_v1
        os.system('sudo apt-get update && sudo apt-get --only-upgrade install kubectl google-cloud-sdk google-cloud-sdk-datastore-emulator google-cloud-sdk-pubsub-emulator google-cloud-sdk-app-engine-go google-cloud-sdk-app-engine-java google-cloud-sdk-app-engine-python google-cloud-sdk-cbt google-cloud-sdk-bigtable-emulator google-cloud-sdk-datalab')

    else:  # mac

        from google.cloud import pubsub_v1 as pubsub_v1
        os.system('gcloud components update')

    PROJECT_NAME = "SheetMuse"
    SUBSCRIPTION_NAME = "monitor_sheetmuse_storage_bucket"

    firebase = firebase.FirebaseApplication(
        'https://sheetmuse.firebaseio.com/')
    receive_messages(PROJECT_NAME, SUBSCRIPTION_NAME)
