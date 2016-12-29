import gzip
import requests
import simplejson

from .exception import APIError

try:
    basestring
except NameError:
    basestring = str


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

    
def api_request(key, function, params=None, data=None, base_url='https://api.shodan.io', method='get', retries=1):
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
    tries = 0
    error = False
    while tries <= retries:
        try:
            if method.lower() == 'post':
                data = requests.post(base_url + function, simplejson.dumps(data), params=params, headers={'content-type': 'application/json'})
            elif method.lower() == 'delete':
                data = requests.delete(base_url + function, params=params)
            else:
                data = requests.get(base_url + function, params=params)

            # Exit out of the loop
            break
        except:
            error = True
            tries += 1

    if error and tries >= retries:
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
    if type(data) == dict and data.get('error', None):
        raise APIError(data['error'])
    
    # Return the data
    return data


def iterate_files(files):
    """Loop over all the records of the provided Shodan output file(s)."""
    if isinstance(files, basestring):
        files = [files]
    
    for filename in files:
        # Create a file handle depending on the filetype
        if filename.endswith('.gz'):
            fin = gzip.open(filename, 'r')
        else:
            fin = open(filename, 'r')

        for line in fin:
            # Convert the JSON into a native Python object
            banner = simplejson.loads(line)
            yield banner

def get_screenshot(banner):
    if 'opts' in banner and 'screenshot' in banner['opts']:
        return banner['opts']['screenshot']
    return None


def get_ip(banner):
    if 'ipv6' in banner:
        return banner['ipv6']
    return banner['ip_str']


def open_file(filename, mode='a', compresslevel=9):
    return gzip.open(filename, mode, compresslevel)


def write_banner(fout, banner):
    line = simplejson.dumps(banner) + '\n'
    fout.write(line.encode('utf-8'))
