import pprint
from django.core.management.base import BaseCommand

from knowledge.models import Entity
from knowledge.utils import fetch_from_remote, pretty_list


def console(message):
    pp = pprint.PrettyPrinter(depth=3)
    pp.pprint(message)



def is_match(term, text):
    """
    :param terms:
    :param text_list:
    :return:
    """
    if text.find(term) != -1:
        return True
    return False


class Command(BaseCommand):
    """
    handles search. also need to search remotely.
    """

    def add_arguments(self, parser):

        parser.add_argument('query',
                            help='supply a valid query. query can contain multiple strings separated by + sign')
        parser.add_argument('--remote', help='switch to search remotely')

    def handle(self, *args, **options):
        terms = str(options['query']).split('+')
        if options['remote']:
            content_tuple_list = fetch_from_remote()
        else:
            content_tuple_list = Entity.objects.all().values_list('key', 'detail')
        output = []
        for content in content_tuple_list:
            for term in terms:
                if is_match(term, content[0]) or is_match(term, content[1]):
                    output.append(content)
                    break
        pretty_list(output)
