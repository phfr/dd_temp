"""
Name management module for the DataDiVR-Backend.

This module provides functionality for managing and generating unique names
for clients in the DataDiVR-Backend system.
"""

import random
from typing import Set


class NameManager:
    """
    A class to manage and generate unique names for clients.

    This class maintains a list of predefined first names and provides
    methods to generate unique names, even when all predefined names are taken.
    """

    def __init__(self):
        """
        Initialize the NameManager with a predefined list of first names.
        """
        self.first_names = [
            "Gerry",
            "Rambo",
            "Katze",
            "Peter",
            "Johnny",
            "Frank",
            "Arnold",
            "Hans",
            "Ivy",
            "Jack",
            "Kate",
            "Liam",
            "Mia",
            "Noah",
            "Olivia",
            "Gonzales",
        ]

    def get_unique_name(self, used_names: Set[str]) -> str:
        """
        Get a unique first name that's not in the used_names set.

        If all predefined names are taken, this method will append a number
        to a randomly chosen name to ensure uniqueness.

        Args:
            used_names (Set[str]): A set of names that are already in use.

        Returns:
            str: A unique name not present in the used_names set.
        """
        available_names = list(set(self.first_names) - used_names)
        if available_names:
            return random.choice(available_names)
        else:
            # If all names are taken, append a number to a random name
            base_name = random.choice(self.first_names)
            suffix = 1
            while f"{base_name}{suffix}" in used_names:
                suffix += 1
            return f"{base_name}{suffix}"


# Create a global instance of NameManager
name_manager = NameManager()
