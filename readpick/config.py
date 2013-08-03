import pkg_resources


class Config(object):

    config = {}

    def __init__(self):
        configuration = pkg_resources.resource_string('readpick', 'api-access.conf')
        exec configuration in self.config

    def pocket_v3_consumer_key(self):
        return self.config['pocket_v3_consumer_key']

    def pocket_v2_key_api(self):
        return self.config['pocket_v2_api_key']