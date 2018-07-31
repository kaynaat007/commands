import json
import os

from django.conf import settings
from knowledge.mqtt import MqttClient
from knowledge.constants import


def get_identity():
    """
    fetches identity of this system
    """
    with open(os.path.join(settings.BASE_DIR, 'identity.json'), 'r') as f:
        identity = json.load(f)
        if not identity:
            raise Exception('You are not registered. run [cheat register] command to register yourself')
    return identity['username']


def fetch_from_remote():
    client = MqttClient(cheat_master_publisher=True)
    verdict = client.publish_message()
    return []


def register_remote(username, email):
    return True


def pretty_dict(mydictlist):

    print(">>>>>>>>>>>>>>>>>>>>>>>>>> {0} RESULTS <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<".format(len(mydictlist)))
    for my_dict in mydictlist:
        for key, value in my_dict.iteritems():
            print("key ===> {0}".format(key))
            print ("value ===> {0}".format(value))
            print("-----------------------------------------------------------------------------")


def pretty_list(mylist):

    print(">>>>>>>>>>>>>>>>>>>>>>>>>> {0} RESULTS <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<".format(len(mylist)))
    for l in mylist:
        print("key ===> {0}".format(l[0]))
        print ("value ===> {0}".format(l[1]))
        print("-----------------------------------------------------------------------------")

