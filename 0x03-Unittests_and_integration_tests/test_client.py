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
        ("google", {"login": "google", "id": 1, "public_repos": 100, "repos_url": "https://api.github.com/orgs/google/repos"}),
        ("abc", {"login": "abc", "id": 2, "public_repos": 50, "repos_url": "https://api.github.com/orgs/abc/repos"}),
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

    def test_public_repos_url(self) -> None:
        """
        Tests that GithubOrgClient._public_repos_url returns the expected URL
        based on a mocked org payload.
        """
        # Define a known payload that GithubOrgClient.org should return
        test_payload = {"repos_url": "https://api.github.com/orgs/test_org/repos"}

        # Use patch as a context manager to mock client.GithubOrgClient.org
        with unittest.mock.patch('client.GithubOrgClient.org', new_callable=unittest.mock.PropertyMock) as mock_org:
            # Configure the mocked org property to return our test_payload
            mock_org.return_value = test_payload

            # Instantiate GithubOrgClient (the org_name doesn't matter here as org() is mocked)
            github_client = client.GithubOrgClient("some_org")

            # Test that the result of _public_repos_url is the expected one
            # We access it as a property, not a method
            self.assertEqual(github_client._public_repos_url, test_payload["repos_url"])

            # Verify that the org property was called exactly once
            mock_org.assert_called_once()


if __name__ == '__main__':
    unittest.main()

