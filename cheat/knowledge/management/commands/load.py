import json

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from knowledge.models import Entity
from knowledge.utils import get_identity


def console(message):
    pass


class Command(BaseCommand):
    """
    handles show command
    """

    def add_arguments(self, parser):
        parser.add_argument('-path', help='The path for content.json file')

    def handle(self, *args, **options):

        username = get_identity()
        user = User.objects.get_by_natural_key(username)
        if options['path']:
            path = options['path']
        else:
            path = 'content.json'

        with open(path, 'r') as f:
            data = json.load(f)

        for detail in data:

            key = detail['key']
            detail = detail['detail']

            entity, is_created = Entity.objects.get_or_create(key=key)
            if is_created:
                entity.created_by = user
            else:
                entity.updated_by = user
            entity.detail = detail
            entity.save()
            print ('saved')

