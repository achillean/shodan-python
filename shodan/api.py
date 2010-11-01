from json       import dumps, loads
from urllib2    import urlopen
from urllib     import urlencode

__all__ = ['WebAPI']

class WebAPIError(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return self.value


class WebAPI:
    """Wrapper around the SHODAN webservices API"""
    
    class ExploitDb:
        
        def __init__(self, parent):
            self.parent = parent
        
        def download(self, id):
            return self.parent._request('exploitdb/download', {'id': id})
        
        def search(self, query, **kwargs):
            return self.parent._request('exploitdb/search', dict(q=query, **kwargs))
    
    def __init__(self, key):
        """Initializes the API object.
        
        Arguments:
        key -- your API key
        
        """
        self.api_key = key
        self.base_url = 'http://www.shodanhq.com/api/'
        self.exploitdb = self.ExploitDb(self)
    
    def _request(self, function, params):
        """General-purpose function to create web requests to SHODAN.
        
        Arguments:
        function  -- name of the function you want to execute
        params      -- dictionary of parameters for the function
        
        Returns
        A JSON string containing the function's results.
        
        """
        # Add the API key parameter automatically
        params['key'] = self.api_key
        
        # Send the request
        data = urlopen(self.base_url + function + '?' + urlencode(params)).read()
        
        # Parse the text into JSON
        data = loads(data)
        
        # Raise an exception if an error occurred
        if data.get('error', None):
            raise WebAPIError(data['error'])
        
        # Return the data
        return data
    
    def fingerprint(self, banner):
        """Determine the software based on the banner.
        
        Arguments:
        banner  - HTTP banner
        
        Returns:
        A list of software that matched the given banner.
        """
        return self._request('fingerprint', {'banner': banner})
    
    def host(self, ip):
        """Get all available information on an IP.

        Arguments:
        ip    -- IP of the computer

        Returns:
        All available information SHODAN has on the given IP,
        subject to API key restrictions.

        """
        return self._request('host', {'ip': ip})
    
    def search(self, query):
        """Search the SHODAN database.
        
        Arguments:
        query    -- search query; identical syntax to the website
        
        Returns:
        A dictionary with 3 main items: matches, countries and total.
        Visit the website for more detailed information.
        
        """
        return self._request('search', {'q': query})
