import requests
import simplejson

import shodan.exception

class Stream:

    base_url = 'https://stream.shodan.io'

    def __init__(self, api_key):
        self.api_key = api_key

    def _create_stream(self, name):
        try:
            req = requests.get(self.base_url + name, params={'key': self.api_key}, stream=True)
        except:
            raise exception.APIError('Unable to contact the Shodan Streaming API')

        if req.status_code != 200:
            try:
                raise exception.APIError(data.json()['error'])
            except:
                pass
            raise exception.APIError('Invalid API key or you do not have access to the Streaming API')
        return req

    def alert(self, aid=None):
        if aid:
            stream = self._create_stream('/shodan/alert/%s' % aid)
        else:
            stream = self._create_stream('/shodan/alert')

        for line in stream.iter_lines():
            if line:
                banner = simplejson.loads(line)
                yield banner

    def banners(self):
        """A real-time feed of the data that Shodan is currently collecting. Note that this is only available to
        API subscription plans and for those it only returns a fraction of the data.
        """
        stream = self._create_stream('/shodan/banners')
        for line in stream.iter_lines():
            if line:
                banner = simplejson.loads(line)
                yield banner

    def ports(self, ports):
        """
        A filtered version of the "banners" stream to only return banners that match the ports of interest.

        :param ports: A list of ports to return banner data on.
        :type ports: int[]
        """
        stream = self._create_stream('/shodan/ports/%s' % ','.join([str(port) for port in ports]))
        for line in stream.iter_lines():
            if line:
                banner = simplejson.loads(line)
                yield banner

    def geo(self):
        """
        A stream of geolocation information for the banners. This is a stripped-down version of the "banners" stream
        in case you only care about the geolocation information.
        """
        stream = self._create_stream('/shodan/geo')
        for line in stream.iter_lines():
            if line:
                banner = simplejson.loads(line)
                yield banner