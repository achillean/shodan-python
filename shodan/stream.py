import requests
import simplejson

import shodan.exception as exception

class Stream:

    base_url = 'https://stream.shodan.io'

    def __init__(self, api_key):
        self.api_key = api_key

    def _create_stream(self, name, timeout=None):
        try:
            req = requests.get(self.base_url + name, params={'key': self.api_key}, stream=True, timeout=timeout)
        except:
            raise exception.APIError('Unable to contact the Shodan Streaming API')

        if req.status_code != 200:
            try:
                req.close()
                raise exception.APIError(data.json()['error'])
            except:
                pass
            raise exception.APIError('Invalid API key or you do not have access to the Streaming API')
        return req

    def alert(self, aid=None, timeout=None):
        if aid:
            stream = self._create_stream('/shodan/alert/%s' % aid, timeout=timeout)
        else:
            stream = self._create_stream('/shodan/alert', timeout=timeout)

        try:
            for line in stream.iter_lines():
                if line:
                    banner = simplejson.loads(line)
                    yield banner
        except requests.exceptions.ConnectionError, e:
            raise exception.APIError('Stream timed out')

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