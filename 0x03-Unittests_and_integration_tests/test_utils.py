#!/usr/bin/env python3
"""
utils.py
A module containing utility functions for various operations, including
nested map access and a simple data processing class.
"""

from typing import Mapping, Sequence, Any, Dict, List

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


if __name__ == "__main__":
    print("--- Self-testing access_nested_map ---")

    # Test case 1
    nested_map_1 = {"a": 1}
    path_1 = ("a",)
    expected_1 = 1
    result_1 = access_nested_map(nested_map_1, path_1)
    print(f"Test 1: Map={nested_map_1}, Path={path_1}, Expected={expected_1}, Result={result_1} -> {'PASSED' if result_1 == expected_1 else 'FAILED'}")
    assert result_1 == expected_1, f"Test 1 Failed: Expected {expected_1}, got {result_1}"

    # Test case 2
    nested_map_2 = {"a": {"b": 2}}
    path_2 = ("a",)
    expected_2 = {"b": 2}
    result_2 = access_nested_map(nested_map_2, path_2)
    print(f"Test 2: Map={nested_map_2}, Path={path_2}, Expected={expected_2}, Result={result_2} -> {'PASSED' if result_2 == expected_2 else 'FAILED'}")
    assert result_2 == expected_2, f"Test 2 Failed: Expected {expected_2}, got {result_2}"

    # Test case 3
    nested_map_3 = {"a": {"b": 2}}
    path_3 = ("a", "b")
    expected_3 = 2
    result_3 = access_nested_map(nested_map_3, path_3)
    print(f"Test 3: Map={nested_map_3}, Path={path_3}, Expected={expected_3}, Result={result_3} -> {'PASSED' if result_3 == expected_3 else 'FAILED'}")
    assert result_3 == expected_3, f"Test 3 Failed: Expected {expected_3}, got {result_3}"

    # Test case 4: Key not found
    nested_map_4 = {"x": {"y": 3}}
    path_4 = ("x", "z")
    print(f"Test 4: Map={nested_map_4}, Path={path_4} (expecting KeyError)")
    try:
        access_nested_map(nested_map_4, path_4)
        print("Test 4: FAILED (KeyError not raised)")
    except KeyError as e:
        print(f"Test 4: PASSED (Caught expected error: {e})")
        assert "Key 'z' not found" in str(e), "Test 4 Failed: Incorrect KeyError message"

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
    print(f"Filtered by city='New York': {filtered_data}")
    assert filtered_data == expected_filtered, "DataProcessor filter_by_key_value FAILED"
    print("DataProcessor filter_by_key_value PASSED")

    # Test get_all_keys
    all_keys = processor.get_all_keys()
    expected_keys = ["city", "id", "name"]
    print(f"All unique keys: {all_keys}")
    assert all_keys == expected_keys, "DataProcessor get_all_keys FAILED"
    print("DataProcessor get_all_keys PASSED")

    print("\nAll self-tests completed.")

