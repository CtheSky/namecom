# encoding=utf-8

import unittest

from namecom import DomainApi
from . import test_env_auth

api = DomainApi(test_env_auth)


class DomainApiTestCase(unittest.TestCase):

    def test_search(self):
        search_result = api.search(keyword='cthesky', timeout=5000)

        results = search_result.results
        self.assertTrue(len(results))
        self.assertTrue(all([_.domainName for _ in results]))
        self.assertTrue(all([_.sld for _ in results]))
        self.assertTrue(all([_.tld for _ in results]))

