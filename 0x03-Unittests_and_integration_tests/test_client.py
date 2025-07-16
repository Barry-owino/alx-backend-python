#!/usr/bin/env python3
"""
client.py
A module containing the GithubOrgClient class for interacting with the GitHub API.
"""

from typing import Dict
from utils import get_json # Import get_json from the utils module

class GithubOrgClient:
    """
    Client for interacting with the public GitHub Organizations API.

    This class provides methods to retrieve information about GitHub organizations.
    """
    def __init__(self, org_name: str) -> None:
        """
        Initializes a GithubOrgClient instance.

        Args:
            org_name (str): The name of the GitHub organization (e.g., "google", "holbertonschool").
        """
        self._org_name = org_name

    def org(self) -> Dict:
        """
        Retrieves the organization's public information from GitHub.

        Constructs the API URL for the organization and uses utils.get_json
        to fetch the data.

        Returns:
            Dict: A dictionary containing the organization's JSON data.
        """
        url = f"https://api.github.com/orgs/{self._org_name}"
        return get_json(url)

# No __main__ block needed for client.py as it's designed to be imported.
