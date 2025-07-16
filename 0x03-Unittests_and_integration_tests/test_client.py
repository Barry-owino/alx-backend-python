#!/usr/bin/env python3
"""
client.py
A module containing the GithubOrgClient class for interacting with the GitHub API.
"""

from typing import Dict, List, Any
from utils import get_json # Import get_json from the utils module

class GithubOrgClient:
    """
    Client for interacting with the public GitHub Organizations API.

    This class provides methods to retrieve information about GitHub organizations
    and their public repositories.
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

    @property
    def _public_repos_url(self) -> str:
        """
        Retrieves the URL for public repositories from the organization's data.

        This is a property that accesses the 'repos_url' key from the
        organization's data obtained via the 'org' method.

        Returns:
            str: The URL to the organization's public repositories.
        """
        return self.org()["repos_url"]

    def public_repos(self) -> List[str]:
        """
        Retrieves a list of public repository names for the organization.

        Fetches the repository data using the _public_repos_url property and
        then extracts the 'name' of each repository.

        Returns:
            List[str]: A list of names of the public repositories.
        """
        repos_payload = get_json(self._public_repos_url)
        return [repo["name"] for repo in repos_payload]
