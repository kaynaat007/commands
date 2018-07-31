import json

from django.conf import settings
from django.core.management.base import BaseCommand

from knowledge.models import Entity
from knowledge.mqtt import MqttClient
from knowledge.utils import get_identity


def console(message):
    pass


class Command(BaseCommand):
    """
    handles show command
    """

    def add_arguments(self, parser):
         pass

    def handle(self, *args, **options):

        flush_unpublished()


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
            'created_by': instance.created_by.username if instance.created_by else None,
            'updated_by': instance.updated_by.username if instance.updated_by else None
        }
        verdict = client.publish_message(settings.ADD_OR_UPDATE_ENTITY, message=json.dumps(data), retain=True, qos=1)
        instance.verdict = verdict
        for_bulk_update.append(instance)
    # trigger sync from master to this slave.
    client.publish_message(settings.FETCH, message=get_identity(),qos=1)
    client.disconnect()