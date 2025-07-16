#!/usr/bin/env python3
"""
utils.py
A module containing utility functions for various operations, including
nested map access and a simple data processing class.
"""

from typing import Mapping, Sequence, Any, Dict, List
import requests # Added import for requests

def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """
    Accesses a value in a nested dictionary (map) using a sequence of keys (path).

    This function iterates through the given path (a sequence of keys) and
    attempts to retrieve the corresponding value from the nested_map.

    Args:
        nested_map (Mapping): The nested dictionary (or map-like object) to traverse.
        path (Sequence): A sequence of keys (e.g., a tuple or list of strings)
                         representing the path to the desired value.

    Returns:
        Any: The value found at the specified path within the nested_map.

    Raises:
        KeyError: If any key in the path is not found in the nested_map
                  at the corresponding level.
    """
    current_value = nested_map
    for key in path:
        if not isinstance(current_value, Mapping) or key not in current_value:
            raise KeyError(f"Key '{key}' not found in the nested map.")
        current_value = current_value[key]
    return current_value


class DataProcessor:
    """
    A simple class for processing and transforming data.

    This class provides basic utilities for data manipulation,
    demonstrating class structure within the module.
    """

    def __init__(self, data: List[Dict[str, Any]]):
        """
        Initializes the DataProcessor with a list of dictionary data.

        Args:
            data (List[Dict[str, Any]]): A list of dictionaries to be processed.
        """
        self.data = data

    def filter_by_key_value(self, key: str, value: Any) -> List[Dict[str, Any]]:
        """
        Filters the internal data list, returning items where a specific key
        matches a given value.

        Args:
            key (str): The key to check in each dictionary.
            value (Any): The value to match against.

        Returns:
            List[Dict[str, Any]]: A new list containing only the filtered dictionaries.
        """
        return [item for item in self.data if item.get(key) == value]

    def get_all_keys(self) -> List[str]:
        """
        Collects all unique keys present across all dictionaries in the data.

        Returns:
            List[str]: A sorted list of unique keys.
        """
        all_keys = set()
        for item in self.data:
            all_keys.update(item.keys())
        return sorted(list(all_keys))

def get_json(url: str) -> Dict:
    """
    Fetches JSON data from a given URL.

    Args:
        url (str): The URL to fetch JSON data from.

    Returns:
        Dict: The JSON response parsed as a dictionary.

    Raises:
        requests.exceptions.RequestException: For network-related errors.
        ValueError: If the response content is not valid JSON.
    """
    response = requests.get(url)
    response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
    return response.json()


if __name__ == "__main__":
    print("--- Self-testing access_nested_map ---")

    # Test case 1
    nested_map_1 = {"a": 1}
    path_1 = ("a",)
    expected_1 = 1
    result_1 = access_nested_map(nested_map_1, path_1)
    test_1_passed = (result_1 == expected_1)
    print(f"Test 1: Map={nested_map_1}, Path={path_1}, Expected={expected_1}, Result={result_1} -> {'PASSED' if test_1_passed else 'FAILED'}")

    # Test case 2
    nested_map_2 = {"a": {"b": 2}}
    path_2 = ("a",)
    expected_2 = {"b": 2}
    result_2 = access_nested_map(nested_map_2, path_2)
    test_2_passed = (result_2 == expected_2)
    print(f"Test 2: Map={nested_map_2}, Path={path_2}, Expected={expected_2}, Result={result_2} -> {'PASSED' if test_2_passed else 'FAILED'}")

    # Test case 3
    nested_map_3 = {"a": {"b": 2}}
    path_3 = ("a", "b")
    expected_3 = 2
    result_3 = access_nested_map(nested_map_3, path_3)
    test_3_passed = (result_3 == expected_3)
    print(f"Test 3: Map={nested_map_3}, Path={path_3}, Expected={expected_3}, Result={result_3} -> {'PASSED' if test_3_passed else 'FAILED'}")

    # Test case 4: Key not found
    nested_map_4 = {"x": {"y": 3}}
    path_4 = ("x", "z")
    print(f"Test 4: Map={nested_map_4}, Path={path_4} (expecting KeyError)")
    test_4_passed = False
    try:
        access_nested_map(nested_map_4, path_4)
        print("Test 4: FAILED (KeyError not raised)")
    except KeyError as e:
        if "Key 'z' not found" in str(e):
            print(f"Test 4: PASSED (Caught expected error: {e})")
            test_4_passed = True
        else:
            print(f"Test 4: FAILED (Caught unexpected KeyError message: {e})")
    except Exception as e:
        print(f"Test 4: FAILED (Caught unexpected exception type: {type(e).__name__}: {e})")


    print("\n--- Self-testing DataProcessor Class ---")
    sample_data = [
        {"id": 1, "name": "Alice", "city": "New York"},
        {"id": 2, "name": "Bob", "city": "London"},
        {"id": 3, "name": "Charlie", "city": "New York"},
        {"id": 4, "name": "David", "city": "Paris"},
    ]
    processor = DataProcessor(sample_data)

    # Test filter_by_key_value
    filtered_data = processor.filter_by_key_value("city", "New York")
    expected_filtered = [{"id": 1, "name": "Alice", "city": "New York"}, {"id": 3, "name": "Charlie", "city": "New York"}]
    test_filter_passed = (filtered_data == expected_filtered)
    print(f"Filtered by city='New York': {filtered_data} -> {'PASSED' if test_filter_passed else 'FAILED'}")

    # Test get_all_keys
    all_keys = processor.get_all_keys()
    expected_keys = ["city", "id", "name"]
    test_keys_passed = (all_keys == expected_keys)
    print(f"All unique keys: {all_keys} -> {'PASSED' if test_keys_passed else 'FAILED'}")

    print("\nAll self-tests completed.")

