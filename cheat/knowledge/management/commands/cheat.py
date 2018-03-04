from django.core.management.base import BaseCommand

from knowledge.models import SystemCommand


def is_match(term, text):
    """
    :param terms:
    :param text_list:
    :return:
    """
    if text.find(term) != -1:
        return True
    return False


def console(*args, **kwargs):
    print("########## output ###########")
    for arg in args:
        if type(arg) == list:
            for x in arg:
                print(x)
        else:
            print(arg)
    for key, value in kwargs.iteritems():
        print(key, value)


class Command(BaseCommand):
    """

    """

    def add_arguments(self, parser):

        parser.add_argument('state', choices=['search', 'add', 'show'], help='supply a given state')
        parser.add_argument('--query', help='supply a query. ')
        parser.add_argument('--cmd',   help='your command')
        parser.add_argument('--detail', help='command detail')

        # args = parser.parse_args()

    def handle(self, *args, **options):
        if options['state'] == 'search':
            if not options['query']:
                console('Must supply query')
                return 
            terms = options['query'].split('+')
            content_tuple_list = SystemCommand.objects.all().values_list('cmd', 'detail')
            output = []
            for content in content_tuple_list:
                for term in terms:
                    if is_match(term, content[0]) or is_match(term, content[1]):
                        output.append(content)
                        break
            console(output)

        elif options['state'] == 'add':
            if not options['cmd'] or not options['detail']:
                console('Supply cmd and detail')
                return 
            instance, is_created = SystemCommand.objects.get_or_create(cmd=options['cmd'])
            instance.detail = options['detail']
            instance.save()
            console('command added')

        elif options['state'] == 'show':
            instances = SystemCommand.objects.all()
            output = []
            for instance in instances:
                output.append({
                    'cmd': instance.cmd,
                    'detail': instance.detail
                })
            console(output)
        else:
            console('invalid state')
