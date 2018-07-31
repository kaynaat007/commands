import json

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from knowledge.utils import register_remote



def console(message):
    print(message)


class Command(BaseCommand):

    def add_arguments(self, parser):

        parser.add_argument('username',  help='supply a string as username')
        parser.add_argument('email', help='supply valid email')

    def handle(self, *args, **options):

        username = options['username']
        email = options['email']
        user, is_created = User.objects.get_or_create(username=username)
        if not is_created:
            console('you are already registered. Updating your email')
        user.email = email
        user.save()
        updated_identity(username, email)
        console('you are registered')
        register_remote(username, email)


def updated_identity(username, email):

    with open('identity.json', 'w') as f:
        data = {
            'username': username,
            'email': email
        }
        json.dump(data, f)
    console('identity updated')