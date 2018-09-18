import unittest
import shodan

try:
    basestring
except NameError:
    basestring = str


class ShodanTests(unittest.TestCase):

	api = None
	FACETS = [
		'port',
		('domain', 1)
	]
	QUERIES = {
		'simple': 'cisco-ios',
		'minify': 'apache',
		'advanced': 'apache port:443',
		'empty': 'asdasdasdasdasdasdasdasdasdhjihjkjk',
	}

	def setUp(self):
		self.api = shodan.Shodan(open('SHODAN-API-KEY').read().strip())

	def test_search_simple(self):
		results = self.api.search(self.QUERIES['simple'])

		# Make sure the properties exist
		self.assertIn('matches', results)
		self.assertIn('total', results)

		# Make sure no error occurred
		self.assertNotIn('error', results)

		# Make sure some values were returned
		self.assertTrue(results['matches'])
		self.assertTrue(results['total'])

		# A regular search shouldn't have the optional info
		self.assertNotIn('opts', results['matches'][0])

	def test_search_empty(self):
		results = self.api.search(self.QUERIES['empty'])
		self.assertTrue(len(results['matches']) == 0)
		self.assertEqual(results['total'], 0)

	def test_search_facets(self):
		results = self.api.search(self.QUERIES['simple'], facets=self.FACETS)

		self.assertTrue(results['facets']['port'])
		self.assertEqual(len(results['facets']['domain']), 1)

	def test_count_simple(self):
		results = self.api.count(self.QUERIES['simple'])

		# Make sure the properties exist
		self.assertIn('matches', results)
		self.assertIn('total', results)

		# Make sure no error occurred
		self.assertNotIn('error', results)

		# Make sure no values were returned
		self.assertFalse(results['matches'])
		self.assertTrue(results['total'])

	def test_count_facets(self):
		results = self.api.count(self.QUERIES['simple'], facets=self.FACETS)

		self.assertTrue(results['facets']['port'])
		self.assertEqual(len(results['facets']['domain']), 1)

	def test_host_details(self):
		host = self.api.host('147.228.101.7')

		self.assertEqual('147.228.101.7', host['ip_str'])
		self.assertFalse(isinstance(host['ip'], basestring))

	def test_search_minify(self):
		results = self.api.search(self.QUERIES['minify'], minify=False)
		self.assertIn('opts', results['matches'][0])

	def test_exploits_search(self):
		results = self.api.exploits.search('apache')
		self.assertIn('matches', results)
		self.assertIn('total', results)
		self.assertTrue(results['matches'])

	def test_exploits_search_paging(self):
		results = self.api.exploits.search('apache', page=1)
		match1 = results['matches'][0]
		results = self.api.exploits.search('apache', page=2)
		match2 = results['matches'][0]

		self.assertNotEqual(match1['_id'], match2['_id'])

	def test_exploits_search_facets(self):
		results = self.api.exploits.search('apache', facets=['source', ('author', 1)])
		self.assertIn('facets', results)
		self.assertTrue(results['facets']['source'])
		self.assertTrue(len(results['facets']['author']) == 1)

	def test_exploits_count(self):
		results = self.api.exploits.count('apache')
		self.assertIn('matches', results)
		self.assertIn('total', results)
		self.assertTrue(len(results['matches']) == 0)

	def test_exploits_count_facets(self):
		results = self.api.exploits.count('apache', facets=['source', ('author', 1)])
		self.assertEqual(len(results['matches']), 0)
		self.assertIn('facets', results)
		self.assertTrue(results['facets']['source'])
		self.assertTrue(len(results['facets']['author']) == 1)

	# Test error responses
	def test_invalid_key(self):
		api = shodan.Shodan('garbage')
		raised = False
		try:
			api.search('something')
		except shodan.APIError as e:
			raised = True

		self.assertTrue(raised)

	def test_invalid_host_ip(self):
		raised = False
		try:
			host = self.api.host('test')
		except shodan.APIError as e:
			raised = True

		self.assertTrue(raised)

	def test_search_empty_query(self):
		raised = False
		try:
			self.api.search('')
		except shodan.APIError as e:
			raised = True
		self.assertTrue(raised)

	def test_search_advanced_query(self):
		# The free API plan can't use filters
		raised = False
		try:
			self.api.search(self.QUERIES['advanced'])
		except shodan.APIError as e:
			raised = True
		self.assertTrue(raised)


if __name__ == '__main__':
    unittest.main()
