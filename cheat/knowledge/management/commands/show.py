from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from knowledge.models import Entity
from knowledge.utils import fetch_from_remote, pretty_list


def console(message):
    print(message)


class Command(BaseCommand):
    """
    handles show command
    """

    def add_arguments(self, parser):
        parser.add_argument('-remote', help='switch to show data from remote.')

    def handle(self, *args, **options):

        if options['remote']:
            # handle remote show here.
            output = fetch_from_remote()
            console(output)
            return
        else:
            output = []
            instances = Entity.objects.all()
        for instance in instances:
                output.append((instance.key, instance.detail))
        if not output:
            console('You can try --remote option to fetch data from remote')
        pretty_list(output)
