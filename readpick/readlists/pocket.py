import json
import logging
import urllib2
from readpick.config import Config

logger = logging.getLogger(__name__)


class Pocket2:
    """
    Pocket v2 API (deprecated)
    """
    base_api_url = 'https://readitlaterlist.com/v2/'
    api_key = Config().pocket_v2_key_api()

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_list(self):
        api_url = 'get?username=%s&password=%s&apikey=%s&count=10&state=unread'

        response = urllib2.urlopen(url=''.join([self.base_api_url,
                                                api_url % (self.username, self.password, self.api_key)]))

        response_json = json.loads(response.read())
        return [{'url': response_json['list'][item_id]['url'],
                 'title': response_json['list'][item_id]['title']} for item_id in response_json['list']]


class Pocket3:
    """
    Pocket reading list wrapper for Pocket v3 API.

    The authentication flow is as follows

    #get request token
    curl -v \
    -XPOST \
    -H "Content-type: application/json; charset=UTF8" \
    -H "X-Accept: application/json" \
    https://getpocket.com/v3/oauth/request \
    -d '{"consumer_key":"17133-80559367051e5861029eba64", "redirect_uri":"authorised"}'

    #authorize application
    https://getpocket.com/auth/authorize?request_token=2dd5391c-cabf-313d-949f-d6442b&redirect_uri=http://mini.wp.pl
    onSuccess: HTTP/1.1 302 Found
    onFailure (needs authorising): HTTP/1.1 200 OK

    # convert request token to access token
    curl -v \
    -XPOST \
    -H "Content-type: application/json; charset=UTF8" \
    -H "X-Accept: application/json" \
    https://getpocket.com/v3/oauth/authorize \
    -d '{"consumer_key":"17133-80559367051e5861029eba64", "code":"2dd5391c-cabf-313d-949f-d6442b"}'


    #make a call
    curl -v \
    -XPOST \
    -H "Content-type: application/json; charset=UTF8" \
    -H "X-Accept: application/json" \
    https://getpocket.com/v3/get \
    -d '{"consumer_key":"17133-80559367051e5861029eba64", "access_token":"cd9516fb-2865-d68e-6ada-e5727f", "count":1}'

    """
    base_api_url = 'https://getpocket.com/v3/'
    authorize_url = 'https://getpocket.com/auth/authorize?request_token=%s&redirect_uri=http://mini.wp.pl'
    consumer_key = Config().pocket_v3_consumer_key()
    access_token = None

    def __init__(self, username=None, password=None):
        print self.consumer_key
        self.username = username
        self.password = password

    def get_request_token(self):
        api_url = 'oauth/request'
        request = urllib2.Request(url=''.join([self.base_api_url, api_url]),
                                 data=json.dumps({'consumer_key': self.consumer_key, 'redirect_uri': 'authorized'}),
                                 headers={'Content-type': 'application/json; charset=UTF8',
                                          'X-Accept': 'application/json'}
        )

        response = urllib2.urlopen(request)

        response_json = json.loads(response.read())
        logger.debug('Request token response: %s' % response_json)
        return response_json['code']

    def is_application_authorized(self, request_token):
        #urllib has never been authorised hence will always return false
        return False

    def  authorize_application(self, request_token):
        import webbrowser
        import threading
        threading.Thread(target=lambda: webbrowser.open_new_tab(self.authorize_url % request_token)).start()
        raw_input('')

    def authorize_session(self):
        api_url = 'oauth/authorize'

        request_token = self.get_request_token()

        if self.is_application_authorized(request_token) is False:
            self.authorize_application(request_token)

        request = urllib2.Request(url=''.join([self.base_api_url, api_url]),
                                 data=json.dumps({'consumer_key': self.consumer_key, 'code': request_token}),
                                 headers={'Content-type': 'application/json; charset=UTF8',
                                          'X-Accept': 'application/json'}
        )

        response = urllib2.urlopen(request)

        response_json = json.loads(response.read())
        logger.debug('Authorize response: %s' % response_json)
        return response_json['access_token']

    def get_list(self):
        api_url = 'get'
        if self.access_token is None:
            self.access_token = self.authorize_session()

        request = urllib2.Request(url=''.join([self.base_api_url, api_url]),
                                  data=json.dumps({'consumer_key': self.consumer_key,
                                                   'access_token': self.access_token,
                                                   'count': 10}),
                                  headers={'Content-type': 'application/json; charset=UTF8',
                                           'X-Accept': 'application/json'}
        )

        response = urllib2.urlopen(request)
        response_json = json.loads(response.read())
        return [{'url': response_json['list'][item_id]['resolved_url'],
                  'title': response_json['list'][item_id]['resolved_title']} for item_id in response_json['list']]