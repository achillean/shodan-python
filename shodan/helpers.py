
import requests
import shodan.exception
import simplejson

def create_facet_string(facets):
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

    
def api_request(key, function, params=None, data=None, base_url='https://api.shodan.io', method='get'):
    """General-purpose function to create web requests to SHODAN.
    
    Arguments:
        function  -- name of the function you want to execute
        params    -- dictionary of parameters for the function
    
    Returns
        A dictionary containing the function's results.
    
    """
    # Add the API key parameter automatically
    params['key'] = key

    # Send the request
    try:
        if method.lower() == 'post':
            data = requests.post(base_url + function, simplejson.dumps(data), params=params, headers={'content-type': 'application/json'})
        elif method.lower() == 'delete':
            data = requests.delete(base_url + function, params=params)
        else:
            data = requests.get(base_url + function, params=params)
    except:
        raise shodan.exception.APIError('Unable to connect to Shodan')

    # Check that the API key wasn't rejected
    if data.status_code == 401:
        try:
            raise shodan.exception.APIError(data.json()['error'])
        except:
            pass
        raise shodan.exception.APIError('Invalid API key')
    
    # Parse the text into JSON
    try:
        data = data.json()
    except:
        raise shodan.exception.APIError('Unable to parse JSON response')
    
    # Raise an exception if an error occurred
    if type(data) == dict and data.get('error', None):
        raise shodan.exception.APIError(data['error'])
    
    # Return the data
    return data