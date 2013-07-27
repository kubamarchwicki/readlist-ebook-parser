from pocket import Pocket


def reading_list_provider(args):
    if args['list_site'] == 'pocket':
        return Pocket(args)