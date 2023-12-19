import abc
import logging
import os
from typing import Tuple, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StringSorter(abc.ABC):
    """
    Abstract base class for sorting strings from an input file and writing the sorted result to an output file.

    Parameters:
    - input_file (str): Path to the input file containing unsorted strings.
    - output_file (str): Path to the output file where sorted strings will be written.
    """

    def __init__(self, input_file: str, output_file: str):
        self.input_file = input_file
        self.output_file = output_file

    def _validate_file_exists(self):
        """
        Validate the existence of the input file and create the output file directory if it does not exist.

        Raises:
        - FileNotFoundError: If the input file is not found.
        """
        if not os.path.exists(self.input_file):
            raise FileNotFoundError(f"Input file not found: {self.input_file}")

        if not os.path.exists(os.path.dirname(self.output_file)):
            os.makedirs(os.path.dirname(self.output_file))
            logger.info(f"Created directory: {os.path.dirname(self.output_file)}")

    def _read_strings(self) -> List[str]:
        """
        Read strings from the input file.

        Returns:
        - List[str]: List of strings read from the input file.
        """
        with open(self.input_file, "r") as file:
            return file.read().splitlines()

    @abc.abstractmethod
    def _custom_sort(self, string: str) -> Tuple[int, str]:
        """
        Abstract method for defining a custom sorting key for strings.

        Parameters:
        - string (str): The string to be sorted.

        Returns:
        - Tuple[int, str]: A tuple containing the numeric and non-numeric parts of the string for sorting.
        """
        raise NotImplementedError

    def _sort_strings(self, strings: List[str]) -> List[str]:
        """
        Sort a list of strings using the custom sorting key.

        Parameters:
        - strings (List[str]): List of strings to be sorted.

        Returns:
        - List[str]: List of sorted strings.
        """
        return sorted(strings, key=self._custom_sort)

    def _write_sorted_strings(self, sorted_strings: List[str]) -> None:
        """
        Write sorted strings to the output file.

        Parameters:
        - sorted_strings (List[str]): List of strings to be written to the output file.
        """
        with open(self.output_file, "w") as file:
            file.write("\n".join(sorted_strings))

    def execute(self) -> None:
        """
        Execute the string sorting process.

        Logs information about the execution, reads strings from the input file, sorts them, and writes
        the sorted strings to the output file.
        """
        logger.info(f"Executing StringSorter with input file: {self.input_file}")
        self._validate_file_exists()

        strings = self._read_strings()
        logger.info(f"Read {len(strings)} strings from input file")

        sorted_strings = self._sort_strings(strings)
        logger.info("Strings sorted successfully")

        self._write_sorted_strings(sorted_strings)
        logger.info(f"Sorted strings written to output file: {self.output_file}")
