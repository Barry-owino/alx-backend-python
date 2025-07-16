My New Python Project
Project Overview
This project serves as a practical demonstration of adhering to strict Python coding standards and best practices, focusing on unit testing and utility function development. It showcases how to write clean, well-documented, and testable Python code.

Purpose
The primary goals of this project are:

To implement a robust utility function for accessing nested data structures.

To develop comprehensive unit tests for this utility function using the unittest framework and parameterized decorator.

To ensure all code strictly follows specified coding style guidelines, documentation standards, and executability requirements.

Project Structure and Contents
utils.py:

Contains general utility functions.

Currently implements access_nested_map, a function designed to safely retrieve values from deeply nested dictionaries using a sequence of keys.

test_utils.py:

Contains unit tests for the functions defined in utils.py.

Includes the TestAccessNestedMap class with parameterized tests for access_nested_map, ensuring its correctness across various valid inputs.

README.md: (This file)

Provides an overview of the project, its purpose, contents, and instructions for setup and execution.

Requirements
All code in this project adheres to the following strict requirements:

Environment: Interpreted/compiled on Ubuntu 18.04 LTS using python3 (version 3.7).

File Endings: All files must end with a new line.

Shebang: The first line of all Python files must be #!/usr/bin/env python3.

Coding Style: Code follows pycodestyle style (version 2.5).

Executability: All Python files must be executable (chmod u+x filename.py).

Documentation (Docstrings):

All modules must have a documentation string.

All classes must have a documentation string.

All functions (inside and outside a class) must have a documentation string.

Documentation strings must be real sentences explaining the purpose.

Type Annotations: All functions and coroutines must be type-annotated.

How to Run and Test
To run the utility function examples and execute the unit tests, follow these steps:

Navigate to the project root directory in your terminal.

Ensure Python 3.7 is available on your system.

Install necessary libraries:

pip install parameterized

Make Python files executable:

chmod u+x utils.py
chmod u+x test_utils.py

Run utils.py (to see the utility function in action):

./utils.py

Run the unit tests:

python3 -m unittest test_utils.py

You should see output indicating that all tests have passed successfully.
