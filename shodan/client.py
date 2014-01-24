# -*- coding: utf-8 -*-

"""
shodan.client
~~~~~~~~~~~~~

This module implements the Shodan API.

:copyright: (c) 2014 by John Matherly
"""

import requests
import simplejson


class APIError(Exception):
    """This exception gets raised whenever a non-200 status code was returned by the Shodan API."""
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return self.value


class Shodan:
    """Wrapper around the Shodan REST and Streaming APIs

    :param key: The Shodan API key that can be obtained from your account page (https://account.shodan.io)
    :type key: str
    :ivar exploits: An instance of `shodan.Shodan.Exploits` that provides access to the Exploits REST API.
    :ivar stream: An instance of `shodan.Shodan.Stream` that provides access to the Streaming API.
    """
    
    class Exploits:

        def __init__(self, parent):
            self.parent = parent
            
        def search(self, query, page=1, facets=None):
            """Search the entire Shodan Exploits archive using the same query syntax
            as the website.
            
            :param query: The exploit search query; same syntax as website.
            :type query: str
            :param facets: A list of strings or tuples to get summary information on.
            :type facets: str
            :param page: The page number to access.
            :type page: int
            :returns: dict -- a dictionary containing the results of the search.
            """
            query_args = {
                'query': query,
                'page': page,
            }
            if facets:
                facet_str = self.parent._create_facet_string(facets)
                query_args['facets'] = facet_str

            return self.parent._request('/api/search', query_args, service='exploits')
            
        def count(self, query, facets=None):
            """Search the entire Shodan Exploits archive but only return the total # of results,
            not the actual exploits.
            
            :param query: The exploit search query; same syntax as website.
            :type query: str
            :param facets: A list of strings or tuples to get summary information on.
            :type facets: str
            :returns: dict -- a dictionary containing the results of the search.
            
            """
            query_args = {
                'query': query,
            }
            if facets:
                facet_str = self.parent._create_facet_string(facets)
                query_args['facets'] = facet_str

            return self.parent._request('/api/count', query_args, service='exploits')

    class Stream:

        base_url = 'https://stream.shodan.io'

        def __init__(self, parent):
            self.parent = parent

        def _create_stream(self, name):
            try:
                req = requests.get(self.base_url + name, params={'key': self.parent.api_key}, stream=True)
            except:
                raise APIError('Unable to contact the Shodan Streaming API')

            if req.status_code != 200:
                try:
                    raise APIError(data.json()['error'])
                except:
                    pass
                raise APIError('Invalid API key or you do not have access to the Streaming API')
            return req

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
    
    def __init__(self, key):
        """Initializes the API object.
        
        :param key: The Shodan API key.
        :type key: str
        """
        self.api_key = key
        self.base_url = 'https://api.shodan.io'
        self.base_exploits_url = 'https://exploits.shodan.io'
        self.exploits = self.Exploits(self)
        self.stream = self.Stream(self)
    
    def _request(self, function, params, service='shodan'):
        """General-purpose function to create web requests to SHODAN.
        
        Arguments:
            function  -- name of the function you want to execute
            params    -- dictionary of parameters for the function
        
        Returns
            A dictionary containing the function's results.
        
        """
        # Add the API key parameter automatically
        params['key'] = self.api_key
        
        # Determine the base_url based on which service we're interacting with
        base_url = {
            'shodan': self.base_url,
            'exploits': self.base_exploits_url,
        }.get(service, 'shodan')

        # Send the request
        try:
            data = requests.get(base_url + function, params=params)
        except:
            raise APIError('Unable to connect to Shodan')

        # Check that the API key wasn't rejected
        if data.status_code == 401:
            try:
                raise APIError(data.json()['error'])
            except:
                pass
            raise APIError('Invalid API key')
        
        # Parse the text into JSON
        try:
            data = data.json()
        except:
            raise APIError('Unable to parse JSON response')
        
        # Raise an exception if an error occurred
        if data.get('error', None):
            raise APIError(data['error'])
        
        # Return the data
        return data

    def _create_facet_string(self, facets):
        """Converts a Python list of facets into a comma-separated string that can be understood by
        the Shodan API.
        """
        facet_str = ''
        for facet in facets:
            if isinstance(facet, basestring):
                facet_str += facet
            else:
                facet_str += '%s:%s'  % (facet[0], facet[1])
            facet_str += ','
        return facet_str[:-1]
    
    def count(self, query, facets=None):
        """Returns the total number of search results for the query.

        :param query: Search query; identical syntax to the website
        :type query: str
        :param facets: (optional) A list of properties to get summary information on
        :type facets: str
        
        :returns: A dictionary with 1 main property: total. If facets have been provided then another property called "facets" will be available at the top-level of the dictionary. Visit the website for more detailed information.
        """
        query_args = {
            'query': query,
        }
        if facets:
            facet_str = self._create_facet_string(facets)
            query_args['facets'] = facet_str
        return self._request('/shodan/host/count', query_args)
    
    def host(self, ip, history=False):
        """Get all available information on an IP.

        :param ip: IP of the computer
        :type ip: str
        :param history: (optional) True if you want to grab the historical (non-current) banners for the host, False otherwise.
        :type history: bool
        """
        params = {}
        if history:
            params['history'] = history
        return self._request('/shodan/host/%s' % ip, params)
    
    def info(self):
        """Returns information about the current API key, such as a list of add-ons
        and other features that are enabled for the current user's API plan.
        """
        return self._request('/api-info', {})
    
    def search(self, query, page=1, limit=None, offset=None, facets=None, minify=True):
        """Search the SHODAN database.

        :param query: Search query; identical syntax to the website
        :type query: str
        :param page: (optional) Page number of the search results
        :type page: int
        :param limit: (optional) Number of results to return
        :type limit: int
        :param offset: (optional) Search offset to begin getting results from
        :type offset: int
        :param facets: (optional) A list of properties to get summary information on
        :type facets: str
        :param minify: (optional) Whether to minify the banner and only return the important data
        :type minify: bool
        
        :returns: A dictionary with 2 main items: matches and total. If facets have been provided then another property called "facets" will be available at the top-level of the dictionary. Visit the website for more detailed information.        
        """
        args = {
            'query': query,
            'minify': minify,
        }
        if limit:
            args['limit'] = limit
            if offset:
                args['offset'] = offset
        else:
            args['page'] = page

        if facets:
            facet_str = self._create_facet_string(facets)
            args['facets'] = facet_str
        
        return self._request('/shodan/host/search', args)
