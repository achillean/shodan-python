
Getting Started
===============

Installation
------------------

To get started with the Python library for Shodan, first make sure that you've
`received your API key <https://account.shodan.io>`_. Once that's done,
install the library via the cheeseshop using:

.. code-block:: bash
	
	$ easy_install shodan

Or if you already have it installed and want to upgrade to the latest version:

.. code-block:: bash
	
	$ easy_install -U shodan

It's always safe to update your library as backwards-compatibility is preserved.
Usually a new version of the library simply means there are new methods/ features
available.


Connect to the API
------------------

The first thing we need to do in our code is to initialize the API object:

.. code-block:: python

	import shodan
	
	SHODAN_API_KEY = "insert your API key here"
	
	api = shodan.Shodan(SHODAN_API_KEY)

	
Searching Shodan
----------------

Now that we have our API object all good to go, we're ready to perform a search:

.. code-block:: python
	
	# Wrap the request in a try/ except block to catch errors
	try:
		# Search Shodan
		results = api.search('apache')
		
		# Show the results
		print('Results found: {}'.format(results['total']))
		for result in results['matches']:
			print('IP: {}'.format(result['ip_str']))
			print(result['data'])
			print('')
	except shodan.APIError as e:
		print('Error: {}'.format(e))

Stepping through the code, we first call the :py:func:`Shodan.search` method on the `api` object which
returns a dictionary of result information. We then print how many results were found in total,
and finally loop through the returned matches and print their IP and banner. Each page of search results
contains up to 100 results.

There's a lot more information that gets returned by the function. See below for a shortened example
dictionary that :py:func:`Shodan.search` returns:

.. code-block:: python
	
	{
		'total': 8669969,
		'matches': [
			{
				'data': 'HTTP/1.0 200 OK\r\nDate: Mon, 08 Nov 2010 05:09:59 GMT\r\nSer...',
				'hostnames': ['pl4t1n.de'],
				'ip': 3579573318,
				'ip_str': '89.110.147.239',
				'os': 'FreeBSD 4.4',
				'port': 80,
				'timestamp': '2014-01-15T05:49:56.283713'
			},
			...
		]
	}

Please visit the `REST API documentation <https://developer.shodan.io/api>`_ for the complete list of properties that the methods can return.

It's also good practice to wrap all API requests in a try/ except clause, since any error
will raise an exception. But for simplicity's sake, I will leave that part out from now on.

Looking up a host
-----------------

To see what Shodan has available on a specific IP we can use the :py:func:`Shodan.host` function:

.. code-block:: python
	
	# Lookup the host
	host = api.host('217.140.75.46')
	
	# Print general info
	print("""
		IP: {}
		Organization: {}
		Operating System: {}
	""".format(host['ip_str'], host.get('org', 'n/a'), host.get('os', 'n/a')))
	
	# Print all banners
	for item in host['data']:
		print("""
			Port: {}
			Banner: {}
			
		""".format(item['port'], item['data']))
