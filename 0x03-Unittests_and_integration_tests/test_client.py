#!/usr/bin/env python3
"""
test_client.py
Unit tests for the GithubOrgClient class in the client module.
"""

import unittest
from parameterized import parameterized
import unittest.mock
from typing import Dict, Tuple, Any

# Import the client module containing the GithubOrgClient class
import client

class TestGithubOrgClient(unittest.TestCase):
    """
    Tests for the GithubOrgClient class, specifically focusing on its 'org' method.
    """

    @parameterized.expand([
        ("google", {"login": "google", "id": 1, "public_repos": 100}),
        ("abc", {"login": "abc", "id": 2, "public_repos": 50}),
    ])
    @unittest.mock.patch('client.get_json') # Patch the get_json function within the client module
    def test_org(self, org_name: str, test_payload: Dict, mock_get_json: unittest.mock.Mock) -> None:
        """
        Tests that GithubOrgClient.org returns the correct value
        and that client.get_json is called exactly once with the expected URL.

        Args:
            org_name (str): The organization name to test.
            test_payload (Dict): The dictionary payload that mock_get_json should return.
            mock_get_json (unittest.mock.Mock): The mocked get_json function.
        """
        # Configure the mock object's return value
        # The mock_get_json (which replaces client.get_json) should return an object
        # whose .json() method returns test_payload.
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = test_payload
        mock_get_json.return_value = mock_response

        # Instantiate the client with the current organization name
        github_client = client.GithubOrgClient(org_name)

        # Call the method under test
        result = github_client.org()

        # Define the expected URL that get_json should have been called with
        expected_url = f"https://api.github.com/orgs/{org_name}"

        # Test that the mocked get_json was called exactly once with the expected URL
        mock_get_json.assert_called_once_with(expected_url)

        # Test that the output of GithubOrgClient.org is equal to the test_payload
        self.assertEqual(result, test_payload)

if __name__ == '__main__':
    unittest.main()
