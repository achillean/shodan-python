import gzip
import requests
import json

from .exception import APIError

try:
    basestring
except NameError:
    basestring = str


def read_from_file(file_path):
    """Read in a list of IP addresses from a specified file

    :param file_path: Path to file being parsed
    :type file_path: str
    :returns: list -- List of IP addresses to be queried
    """
    output = list()
    with open(file_path, 'r') as fil:
        output = fil.read().splitlines()

    return output

def create_facet_string(facets):
    """Converts a Python list of facets into a comma-separated string that can be understood by
    the Shodan API.
    """
    facet_str = ''
    for facet in facets:
        if isinstance(facet, basestring):
            facet_str += facet
        else:
            facet_str += '{}:{}'.format(facet[0], facet[1])
        facet_str += ','
    return facet_str[:-1]


def api_request(key, function, params=None, data=None, base_url='https://api.shodan.io',
                method='get', retries=1, proxies=None):
    """General-purpose function to create web requests to SHODAN.

    Arguments:
        function  -- name of the function you want to execute
        params    -- dictionary of parameters for the function
        proxies   -- a proxies array for the requests library

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
                data = requests.post(base_url + function, json.dumps(data), params=params,
                                     headers={'content-type': 'application/json'},
                                     proxies=proxies)
            elif method.lower() == 'delete':
                data = requests.delete(base_url + function, params=params, proxies=proxies)
            elif method.lower() == 'put':
                data = requests.put(base_url + function, params=params, proxies=proxies)
            else:
                data = requests.get(base_url + function, params=params, proxies=proxies)

            # Exit out of the loop
            break
        except Exception:
            error = True
            tries += 1

    if error and tries >= retries:
        raise APIError('Unable to connect to Shodan')

    # Check that the API key wasn't rejected
    if data.status_code == 401:
        try:
            raise APIError(data.json()['error'])
        except (ValueError, KeyError):
            pass
        raise APIError('Invalid API key')

    # Parse the text into JSON
    try:
        data = data.json()
    except Exception:
        raise APIError('Unable to parse JSON response')

    # Raise an exception if an error occurred
    if type(data) == dict and data.get('error', None):
        raise APIError(data['error'])

    # Return the data
    return data


def iterate_files(files, fast=False):
    """Loop over all the records of the provided Shodan output file(s)."""
    loads = json.loads
    if fast:
        # Try to use ujson for parsing JSON if it's available and the user requested faster throughput
        # It's significantly faster at encoding/ decoding JSON but it doesn't support as
        # many options as the standard library. As such, we're mostly interested in using it for
        # decoding since reading/ parsing files will use up the most time.
        # pylint: disable=E0401
        try:
            from ujson import loads
        except Exception:
            pass

    if isinstance(files, basestring):
        files = [files]

    for filename in files:
        # Create a file handle depending on the filetype
        if filename.endswith('.gz'):
            fin = gzip.open(filename, 'r')
        else:
            fin = open(filename, 'r')

        for line in fin:
            # Ensure the line has been decoded into a string to prevent errors w/ Python3
            if not isinstance(line, basestring):
                line = line.decode('utf-8')

            # Convert the JSON into a native Python object
            banner = loads(line)
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
    line = json.dumps(banner) + '\n'
    fout.write(line.encode('utf-8'))


def humanize_bytes(byte_count, precision=1):
    """Return a humanized string representation of a number of bytes.
    >>> humanize_bytes(1)
    '1 byte'
    >>> humanize_bytes(1024)
    '1.0 kB'
    >>> humanize_bytes(1024*123)
    '123.0 kB'
    >>> humanize_bytes(1024*12342)
    '12.1 MB'
    >>> humanize_bytes(1024*12342,2)
    '12.05 MB'
    >>> humanize_bytes(1024*1234,2)
    '1.21 MB'
    >>> humanize_bytes(1024*1234*1111,2)
    '1.31 GB'
    >>> humanize_bytes(1024*1234*1111,1)
    '1.3 GB'
    """
    if byte_count == 1:
        return '1 byte'
    if byte_count < 1024:
        '{0:0.{1}f} {2}'.format(byte_count, 0, 'bytes')

    suffixes = ['KB', 'MB', 'GB', 'TB', 'PB']
    multiple = 1024.0  # .0 to force float on python 2
    for suffix in suffixes:
        byte_count /= multiple
        if byte_count < multiple:
            return '{0:0.{1}f} {2}'.format(byte_count, precision, suffix)
    return '{0:0.{1}f} {2}'.format(byte_count, precision, suffix)
