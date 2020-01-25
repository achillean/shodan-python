GIF Creator
-----------

Shodan keeps a full history of all the information that has been gathered on an IP address. With the API,
you're able to retrieve that history and we're going to use that to create a tool that outputs GIFs made of
the screenshots that the Shodan crawlers gather.

The below code requires the following Python packages:

	- arrow
	- shodan

The **arrow** package is used to parse the *timestamp* field of the banner into a Python `datetime` object.

In addition to the above Python packages, you also need to have the **ImageMagick** software installed. If you're
working on Ubuntu or another distro using **apt** you can run the following command:

.. code-block:: bash
	
	sudo apt-get install imagemagick

This will provide us with the **convert** command which is needed to merge several images into an animated GIF.

There are a few key Shodan methods/ parameters that make the script work:

1. :py:func:`shodan.helpers.iterate_files()` to loop through the Shodan data file
2. **history** flag on the :py:func:`shodan.Shodan.host` method to get all the banners for an IP that Shodan has collected over the years



.. code-block:: python

	#!/usr/bin/env python
	# gifcreator.py
	#
	# Dependencies:
	# - arrow
	# - shodan
	#
	# Installation:
	# sudo easy_install arrow shodan
	# sudo apt-get install imagemagick
	#
	# Usage:
	# 1. Download a json.gz file using the website or the Shodan command-line tool (https://cli.shodan.io).
	#    For example:
	#        shodan download screenshots.json.gz has_screenshot:true
	# 2. Run the tool on the file:
	#        python gifcreator.py screenshots.json.gz
	
	import arrow
	import os
	import shodan
	import shodan.helpers as helpers
	import sys
	
	
	# Settings
	API_KEY = ''
	MIN_SCREENS = 5	# Number of screenshots that Shodan needs to have in order to make a GIF
	MAX_SCREENS = 24
	
	if len(sys.argv) != 2:
		print('Usage: {} <shodan-data.json.gz>'.format(sys.argv[0]))
		sys.exit(1)
	
	# GIFs are stored in the local "data" directory
	os.mkdir('data')
	
	# We need to connect to the API to lookup the historical host information
	api = shodan.Shodan(API_KEY)
	
	# Use the shodan.helpers.iterate_files() method to loop over the Shodan data file
	for result in helpers.iterate_files(sys.argv[1]):
		# Get the historic info
		host = api.host(result['ip_str'], history=True)
		
		# Count how many screenshots this host has
		screenshots = []
		for banner in host['data']:
			# Extract the image from the banner data
			if 'opts' in banner and 'screenshot' in banner['opts']:
				# Sort the images by the time they were collected so the GIF will loop
				# based on the local time regardless of which day the banner was taken.
				timestamp = arrow.get(banner['timestamp']).time()
				sort_key = timestamp.hour
				screenshots.append((
					sort_key,
					banner['opts']['screenshot']['data']
				))
				
				# Ignore any further screenshots if we already have MAX_SCREENS number of images
				if len(screenshots) >= MAX_SCREENS:
					break
		
		# Extract the screenshots and turn them into a GIF if we've got the necessary
		# amount of images.
		if len(screenshots) >= MIN_SCREENS:
			for (i, screenshot) in enumerate(sorted(screenshots, key=lambda x: x[0], reverse=True)):
				open('/tmp/gif-image-{}.jpg'.format(i), 'w').write(screenshot[1].decode('base64'))
			
			# Create the actual GIF using the  ImageMagick "convert" command
			os.system('convert -layers OptimizePlus -delay 5x10 /tmp/gif-image-*.jpg -loop 0 +dither -colors 256 -depth 8 data/{}.gif'.format(result['ip_str']))
	
			# Clean up the temporary files
			os.system('rm -f /tmp/gif-image-*.jpg')
	
			# Show a progress indicator
			print(result['ip_str'])


The full code is also available on GitHub: https://gist.github.com/achillean/963eea552233d9550101
