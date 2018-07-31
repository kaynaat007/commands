import json

from django.core.management.base import BaseCommand

from knowledge.constants import TOPIC_NEW_COMMAND
from knowledge.models import Entity
from knowledge.models import People
from knowledge.mqtt import MqttClient
from knowledge.utils import get_identity


def console(message):
    pass


class Command(BaseCommand):
    """
    handles show command
    """

    def add_arguments(self, parser):

        parser.add_argument('key', nargs='+', help='supply a valid key. keys are unique in the system')
        parser.add_argument('detail', nargs='+', help='supply detail for the key')

    def handle(self, *args, **options):

        username = get_identity()
        user, is_people_created = People.objects.get_or_create(username=username)
        key = options['key']
        detail = options['detail']
        entity, is_created = Entity.objects.get_or_create(key=key)

        if is_created:
            entity.created_by = user
            entity.updated_by = user
        else:
            entity.updated_by = user
            if not entity.created_by:
                entity.created_by = user

        entity.detail = detail
        entity.save()

        data = {
            'key': key,
            'detail': detail,
            'created_by': entity.created_by.username,
            'updated_by': entity.updated_by.username,
            'identity': username
        }

        client = MqttClient(cheat_master_publisher=True)
        verdict = client.publish_message(TOPIC_NEW_COMMAND, data, qos=1)
        if not verdict:
            entity.is_published = False
            entity.save()
        client.disconnect()