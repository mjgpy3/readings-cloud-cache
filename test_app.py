#!/usr/bin/env python

import unittest

from app import build_connection, assert_safe_url

class TestAssertValidUrl(unittest.TestCase):
    def test_given_a_valid_http_url_it_does_nothing(self):
        assert_safe_url('http://www.example.com')

    def test_given_a_valid_https_url_it_does_nothing(self):
        assert_safe_url('https://www.example.com')

    def test_given_a_valid_longer_url_it_does_nothing(self):
        assert_safe_url('https://www.google.com/webhp?sourceid=chrome-instant&ion=1&espv=2&es_th=1&ie=UTF-8#safe=off&q=example+long+url')

    def test_it_errors_when_given_a_url_not_beginning_with_a_valid_scheme(self):
        with self.assertRaises(AssertionError):
            assert_safe_url('ftp://www.example.com')

    def test_it_errors_when_given_a_url_with_a_comment_beginning_in_it(self):
        with self.assertRaises(AssertionError):
            assert_safe_url('http://www.example.com/*')

    def test_it_errors_when_given_a_url_with_a_single_quote(self):
        with self.assertRaises(AssertionError):
            assert_safe_url('http://www.example.\'com/')

    def test_it_errors_when_given_a_url_with_a_space(self):
        with self.assertRaises(AssertionError):
            assert_safe_url('http://www.example.com/ /foobar')

    def test_it_errors_when_given_a_url_with_a_newline(self):
        with self.assertRaises(AssertionError):
            assert_safe_url('http://www.example.com/\n/foobar')

    def test_it_errors_when_given_a_url_with_a_cr(self):
        with self.assertRaises(AssertionError):
            assert_safe_url('http://www.example.com/\r/foobar')

    def test_it_errors_when_given_a_url_with_a_tab(self):
        with self.assertRaises(AssertionError):
            assert_safe_url('http://www.example.com/\t/foobar')

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
