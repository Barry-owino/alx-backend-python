#!/usr/bin/env python3
"""
utils.py
A module containing utility functions for various operations.
"""

from typing import Mapping, Sequence, Any

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

if __name__ == "__main__":
    my_nested_map = {"a": {"b": {"c": 10}}}
    print(f"access_nested_map({my_nested_map}, ('a', 'b', 'c')) -> {access_nested_map(my_nested_map, ('a', 'b', 'c'))}")

    try:
        print(f"access_nested_map({my_nested_map}, ('a', 'x')) -> {access_nested_map(my_nested_map, ('a', 'x'))}")
    except KeyError as e:
        print(f"Caught expected error: {e}")
