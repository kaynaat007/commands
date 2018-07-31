from django.core.management.base import BaseCommand

from knowledge.mqtt import MqttClient

class Command(BaseCommand):
    """
    custom command to run mqtt client.
    """

    def handle(self, *args, **options):

        # We set status of all astros as false and wait for next celery task to send updates.
        # Meanwhile if an astro registers, status will be set to True.
        MqttClient(subscriber=True).run()
        pass
