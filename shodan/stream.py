import requests
import simplejson

from .exception import APIError


class Stream:

    base_url = 'https://stream.shodan.io'

    def __init__(self, api_key):
        self.api_key = api_key

    def _create_stream(self, name, timeout=None):
        try:
            req = requests.get(self.base_url + name, params={'key': self.api_key}, stream=True, timeout=timeout)
        except Exception as e:
            raise APIError('Unable to contact the Shodan Streaming API')

        if req.status_code != 200:
            try:
                data = simplejson.loads(req.text)
                raise APIError(data['error'])
            except APIError as e:
                raise
            except Exception as e:
                pass
            raise APIError('Invalid API key or you do not have access to the Streaming API')
        return req

    def _iter_stream(self, stream, raw):
        for line in stream.iter_lines():
            if line:
                if raw:
                    yield line
                else:
                    yield simplejson.loads(line)

    def alert(self, aid=None, timeout=None, raw=False):
        if aid:
            stream = self._create_stream('/shodan/alert/%s' % aid, timeout=timeout)
        else:
            stream = self._create_stream('/shodan/alert', timeout=timeout)

        try:
            for line in self._iter_stream(stream, raw):
                yield line
        except requests.exceptions.ConnectionError as e:
            raise APIError('Stream timed out')

    def banners(self, raw=False, timeout=None):
        """A real-time feed of the data that Shodan is currently collecting. Note that this is only available to
        API subscription plans and for those it only returns a fraction of the data.
        """
        stream = self._create_stream('/shodan/banners', timeout=timeout)
        for line in self._iter_stream(stream, raw):
            yield line

    def ports(self, ports, raw=False, timeout=None):
        """
        A filtered version of the "banners" stream to only return banners that match the ports of interest.

        :param ports: A list of ports to return banner data on.
        :type ports: int[]
        """
        stream = self._create_stream('/shodan/ports/%s' % ','.join([str(port) for port in ports]), timeout=timeout)
        for line in self._iter_stream(stream, raw):
            yield line
