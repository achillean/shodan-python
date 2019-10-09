Access SSL certificates in Real-Time
------------------------------------

The new Shodan Streaming API provides real-time access to the information that Shodan is gathering at the moment.
Using the Streaming API, you get the raw access to potentially all the data that ends up in the Shodan search engine.
Note that you can't search with the Streaming API or perform any other operations that you're accustomed to with
the REST API. This is meant for large-scale consumption of real-time data.

This script only works with people that have a subscription API plan!
And by default the Streaming API only returns 1% of the data that Shodan gathers.
If you wish to have more access please contact us at support@shodan.io for pricing
information.

.. code-block:: python

	#!/usr/bin/env python
	#
	# cert-stream.py
	# Stream the SSL certificates that Shodan is collecting at the moment
	#
	# WARNING: This script only works with people that have a subscription API plan!
	# And by default the Streaming API only returns 1% of the data that Shodan gathers.
	# If you wish to have more access please contact us at sales@shodan.io for pricing
	# information.
	#
	# Author: achillean
	import shodan
	import sys

	# Configuration
	API_KEY = 'YOUR API KEY'

	try:
	    # Setup the api
	    api = shodan.Shodan(API_KEY)

	    print('Listening for certs...')
	    for banner in api.stream.ports([443, 8443]):
			if 'ssl' in banner:
				# Print out all the SSL information that Shodan has collected
				print(banner['ssl'])
	    
	except Exception as e:
	    print('Error: {}'.format(e))
	    sys.exit(1)
