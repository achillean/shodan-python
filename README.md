## Installation

To install the library from the cheeseshop, you can use easy_install:

	easy_install shodan

Or simply download this repository and run:

	python setup.py install

## Usage

Before you can use the API, you need to have an API key.

[Get your API key here](http://www.shodanhq.com/api_doc)

Setup the SHODAN WebAPI:

	from shodan import WebAPI
	
	api = WebAPI(MY_API_KEY)

Print a list of cisco-ios devices:

	result = api.search("cisco-ios")
	for host in result['matches']:
		print host['ip']

Get all the information SHODAN has on the IP 217.140.75.46:

	host = api.host('217.140.75.46')
	print host

Query ExploitDB (http://www.exploit-db.com) for exploits relating to PHP:
	
	exploits = api.exploitdb.search('PHP')
	print 'Found %s exploits' % exploits['total']
	for exploit in exploits['matches']:
		print exploit

To download the actual exploit code, just follow it up with:

	code = api.exploitdb.download(exploit['id'])
	print 'Name: %s' % code['filename']
	print 'Type: %s' % code['content-type']
	print 'Contents:\n%s' % code['data']

To properly handle potential errors, you should wrap all requests in a try/except block:

	try:
		api.search("cisco-ios")
	except Exception, e:
		print 'Error: %s' % e

## Articles

* [Quick introduction to using the SHODAN API with Python](http://www.surtri.com/2010/08/16/shodan-api-and-unique)
