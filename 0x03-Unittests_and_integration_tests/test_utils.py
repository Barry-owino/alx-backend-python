#!/usr/bin/env python3
"""
test_utils.py
Unit tests for the utility functions in the utils module.
"""

import unittest
from parameterized import parameterized
from typing import Dict, Tuple, Any

# Import the utils module containing the access_nested_map function
import utils

class TestAccessNestedMap(unittest.TestCase):
    """
    Tests for the access_nested_map function in the utils module.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: Dict, path: Tuple, expected: Any) -> None:
        """
        Tests that access_nested_map returns the expected result for various inputs.
        This method uses parameterized testing for multiple test cases.
        """
        self.assertEqual(utils.access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "Key 'a' not found in the nested map."),
        ({"a": 1}, ("a", "b"), "Key 'b' not found in the nested map."),
    ])
    def test_access_nested_map_exception(self, nested_map: Dict, path: Tuple, expected_message: str) -> None:
        """
        Tests that access_nested_map raises a KeyError with the expected message
        for invalid paths or missing keys.
        """
        with self.assertRaisesRegex(KeyError, expected_message):
            utils.access_nested_map(nested_map, path)

if __name__ == '__main__':
    unittest.main()

