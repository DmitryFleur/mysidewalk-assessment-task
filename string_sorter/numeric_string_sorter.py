import re
from typing import Tuple

from string_sorter.string_sorter import StringSorter


class NumericStringSorter(StringSorter):
    def _custom_sort(self, string: str) -> Tuple[int, str]:
        """
        Custom sorting method for sorting strings containing numeric and non-numeric parts.

        This method uses a regular expression to match numeric and non-numeric parts in the string.
        The numeric part is extracted from the match, and if there's a numeric part, it is converted
        to an integer; otherwise, it is set to positive infinity. The non-numeric part is also extracted
        from the match.

        Parameters:
        - string (str): The string to be sorted.

        Returns:
        - Tuple[int, str]: A tuple containing the numeric and non-numeric parts of the string for sorting.
        """
        match = re.match(r"(\d*)(\D*)", string)
        numeric_part = int(match.group(1)) if match.group(1) else float("inf")
        alpha_part = match.group(2)

        return numeric_part, alpha_part
