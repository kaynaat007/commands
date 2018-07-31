import json
import os
import time

from django.conf import settings
from django.contrib.auth.models import User

import paho.mqtt.client as paho
from LogEndPoint.dyfo_logger import getLogger

from models import Entity, People
from knowledge.utils import get_identity
from constants import TOPIC_NEW_COMMAND, SEARCH

logger = getLogger('DYFO_LOGGER', os.path.basename(__file__))


def console(message):
    pass


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


class MqttClient(object):
    __metaclass__ = Singleton

    def __init__(self, subscriber=False, cheat_master_publisher=False):
        self.subscriber = subscriber
        self.cheat_master_publisher = cheat_master_publisher
        self.client = None
        self.identity = get_identity()
        if self.subscriber:
            self.client = paho.Client(settings.MQTT_SUBSCRIBER_BASE_NAME + self.identity)
        elif self.cheat_master_publisher:
            self.client = paho.Client(settings.MQTT_PUBLISHER_BASE_NAME + self.identity)
            self.run()
        if not self.client:
            logger.error('It is an error to call MqttClient with both param as False.')
            raise Exception('It is an error to call MqttClient with both param as False')

    def disconnect(self):

        if self.client:
            self.client.disconnect()

    def run(self):

        try:
            if self.subscriber:

                self.client.on_connect = on_connect
                self.client.on_subscribe = on_subscribe
                self.client.on_message = on_message

            else:
                self.client.on_connect = pub_connect

            self.client.on_disconnect = on_disconnect
            self.client.on_log = on_log
            self.client.is_connected = False
            self.client.connect(settings.MQTT_BROKER_HOST, settings.MQTT_BROKER_PORT)

            if self.subscriber:
                self.client.loop_forever()
            else:
                self.client.loop_start()
            time.sleep(3)
            while True:
                if self.client.is_connected:
                    break
                time.sleep(1)
        except Exception as e:
            logger.exception(str(e))
            self.client.loop_stop()
            self.client.disconnect()

    def publish_message(self, topic, message=None, retain=False, qos=0):
        """
        publishes message on the givrn topic
        :param topic:
        :param message:
        :return:
        """
        if not self.client:
            raise Exception('client not initialized')

        if message is not None:
            string_message = json.dumps(message)
        else:
            string_message = message

        logger.debug({"ACTION": "PUBLISHING_MESSAGE", "TOPIC": topic, "MESSAGE": string_message})

        result, mid = self.client.publish(topic, string_message, retain=retain, qos=qos)

        logger.debug({"ACTION": "PUBLISHED_RESULT", "RESULT": result})
        logger.debug({"ACTION": "PUBLISHED_MID", "RESULT": mid})

        if result == paho.MQTT_ERR_NO_CONN:
            logger.info('client is not connected to broker')
            logger.info('could not publish. Retry publish later')
            return False
            # raise Exception('client is not connected to broker')

        if result == paho.MQTT_ERR_SUCCESS:
            message = 'The message {1} for topic {0} was successfully published'.format(topic, message)
            logger.debug(message)
            return True

        return False


def pub_connect(client, userdata, flags, rc):

    if rc == 0:  # successfully connected
        client.is_connected = True
    else:
        client.is_connected = False
        logger.error('connection not successfull with broker {0}, {1}'.format(settings.MQTT_BROKER_HOST,
                                                                      settings.MQTT_BROKER_PORT))


def on_connect(client, userdata, flags, rc):
    """
    called when the connection set's up
    :param client:
    :param userdata:
    :param flags:
    :param rc:
    :return:
    """

    logger.info('CONNACK received with code %d.' % (rc))
    if rc == 0:  # successfully connected
        topics = [

            (settings.PUSH_ENTITY, 1),
            (settings.SYNC + get_identity(), 1),
            (TOPIC_NEW_COMMAND, 1)
        ]
        client.subscribe(topics)
        client.is_connected = True
        logger.info('subscribing to {0}'.format(topics))
    else:
        client.is_connected = False
        logger.error('connection not successfull with broker {0}, {1}'.format(settings.MQTT_BROKER_HOST,
                                                                              settings.MQTT_BROKER_PORT))


def on_publish(client, userdata, mid):
    """
    called whenever a message is published.
    :param client:
    :param userdata:
    :param mid:
    :return:
    """
    logger.debug('callback called on publish. message id {0}'.format(str(mid)))


def on_subscribe(client, userdata, mid, granted_qos):
    """
    called once the broker responded to a subscription request.
    :param client:
    :param userdata:
    :param mid:
    :param granted_qos:
    :return:
    """
    logger.debug("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(client, userdata, msg):
    """
    called for each message received .
    :param client:
    :param userdata:
    :param msg:
    :return:
    """

    logger.debug('message arrived for topic {0}'.format(msg.topic))
    if msg.topic == settings.PUSH_ENTITY:
        # data has arrived. save it. somebody has updated the master.
        data = json.loads(msg.payload)
        entity, is_created = Entity.objects.get_or_create(key=data['key'])
        detail = data['detail']
        entity.detail = detail
        entity.save()
    if msg.topic == settings.SYNC + get_identity():
        # all master data has arrived. update one by one.
        data = json.loads(msg.payload)
        for entity in data:
            key = entity['key']
            detail = entity['detail']
            instance, is_created = Entity.objects.get_or_create(key=key)
            instance.detail = detail
            instance.save()  # todo: shift to bulk update here

    if msg.topic == TOPIC_NEW_COMMAND:  # when this client receives the new data

        data = json.loads(msg.payload)
        identity = data['identity']
        if identity == get_identity():
            logger.info('Same identity. Not saving')
            return
        entity, is_created = Entity.objects.get_or_create(key=data['key'])
        entity.detail = data['detail']
        entity.created_by = People.objects.get_or_create(username=data['created_by'])[0]
        entity.updated_by = People.objects.get_or_create(username=data['updated_by'])[0]
        entity.save()
        logger.info('data saved')

    if msg.topic == SEARCH:  # listens to search

        data = json.loads(msg.payload)
        target_topic = data['search_result_topic']

        
def flush_unpublished():
    """
    runs to publish the unpublished messages to clients.
    """

    unpublished_instances = Entity.objects.filter(is_published=False)
    if not unpublished_instances:
        return
    client = MqttClient(cheat_master_publisher=True)
    for_bulk_update = []
    for instance in unpublished_instances:
        data = {
            'key': instance.key,
            'detail': instance.detail,
            'created_by': instance.created_by.pk if instance.created_by else None,
            'updated_by': instance.updated_by.pk if instance.updated_by else None
        }
        verdict = client.publish_message(settings.PUSH_ENTITY, message=json.dumps(data), retain=True, qos=1)
        instance.verdict = verdict
        for_bulk_update.append(instance)
    client.disconnect()


def on_disconnect(client, userdata, rc):
    """
    calls whenever disconnect happens
    :param client:
    :param userdata:
    :param rc:
    :return:
    """
    client.is_connected = False

    if rc == 0:  # graceful disconnect
        logger.info('client gracefully disconnected')
    else:
        logger.info('client abnormally disconnected')


def on_log(client, userdata, level, buf):
    logger.debug(buf)
