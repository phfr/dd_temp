import random
from typing import Set


class NameManager:
    def __init__(self):
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
        """Get a unique first name that's not in the used_names set."""
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


name_manager = NameManager()
