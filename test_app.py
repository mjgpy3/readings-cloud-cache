#!/usr/bin/env python

import unittest

from app import build_connection

class TestConnectionBuilder(unittest.TestCase):
    def setUp(self):
        database_url = 'postgres://username:passy@hostyplace.com:5432/databass'
        dummy_connector = lambda: None

        def connector_to_dict(**kwargs):
            return { 'args': kwargs,
                     'identifier': 'DummyConnectorResult' }

        dummy_connector.connect = connector_to_dict

        self.result = build_connection(dummy_connector, database_url)

    def test_build_connection_returns_the_connector_result(self):
        self.assertEqual('DummyConnectorResult', self.result['identifier'])

    def test_build_connection_passes_on_the_port_correctly(self):
        self.assertEqual(5432, self.result['args']['port'])

    def test_build_connection_passes_on_the_username_correctly(self):
        self.assertEqual('username', self.result['args']['user'])

    def test_build_connection_passes_on_the_password_correctly(self):
        self.assertEqual('passy', self.result['args']['password'])

    def test_build_connection_passes_on_the_database_correctly(self):
        self.assertEqual('databass', self.result['args']['database'])

    def test_build_connection_passes_on_the_host_correctly(self):
        self.assertEqual('hostyplace.com', self.result['args']['host'])

if __name__ == '__main__':
    unittest.main()
