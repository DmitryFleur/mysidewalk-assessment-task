import os
import tempfile
import unittest
from tempfile import TemporaryDirectory

from string_sorter.numeric_string_sorter import NumericStringSorter


class TestNumericStringSorter(unittest.TestCase):
    def setUp(self):
        self.test_dir = TemporaryDirectory()
        self.input_file_path = os.path.join(self.test_dir.name, "input.txt")
        self.output_file_path = os.path.join(self.test_dir.name, "output.txt")

        with open(self.input_file_path, "w") as file:
            file.write(
                "2 Steaks\n10 Chicken Wings\n343GuiltySparks\nactivity\nadvertising\n"
                "championship\nconversation\ncriticism\neconomics\ninitiative\n"
                "literature\nmanufacturer\nobligation\nopportunity\npriority\n"
                "secretary\ntelevision\nunderstanding"
            )

    def tearDown(self):
        self.test_dir.cleanup()

    def test_execute(self):
        sorter = NumericStringSorter(self.input_file_path, self.output_file_path)
        sorter.execute()

        with open(self.output_file_path, "r") as file:
            sorted_strings = file.read().splitlines()

        expected_sorted_strings = [
            "2 Steaks",
            "10 Chicken Wings",
            "343GuiltySparks",
            "activity",
            "advertising",
            "championship",
            "conversation",
            "criticism",
            "economics",
            "initiative",
            "literature",
            "manufacturer",
            "obligation",
            "opportunity",
            "priority",
            "secretary",
            "television",
            "understanding",
        ]
        self.assertEqual(sorted_strings, expected_sorted_strings)

    def test_sort_and_write_empty_input(self):
        # Create an empty input file
        with open(self.input_file_path, "w") as file:
            file.write("")

        sorter = NumericStringSorter(self.input_file_path, self.output_file_path)
        sorter.execute()

        with open(self.output_file_path, "r") as file:
            sorted_strings = file.read().splitlines()

        # The output should also be empty
        self.assertEqual(sorted_strings, [])

    def test_sort_and_write_numeric_input_only(self):
        # Create an input file with only numeric strings
        with open(self.input_file_path, "w") as file:
            file.write("3\n1\n10\n5\n")

        sorter = NumericStringSorter(self.input_file_path, self.output_file_path)
        sorter.execute()

        with open(self.output_file_path, "r") as file:
            sorted_strings = file.read().splitlines()

        expected_sorted_strings = ["1", "3", "5", "10"]
        self.assertEqual(sorted_strings, expected_sorted_strings)

    def test_sort_and_write_non_numeric_input_only(self):
        # Create an input file with only non-numeric strings
        with open(self.input_file_path, "w") as file:
            file.write("apple\norange\nbanana\npear\n")

        sorter = NumericStringSorter(self.input_file_path, self.output_file_path)
        sorter.execute()

        with open(self.output_file_path, "r") as file:
            sorted_strings = file.read().splitlines()

        expected_sorted_strings = ["apple", "banana", "orange", "pear"]
        self.assertEqual(sorted_strings, expected_sorted_strings)

    def test_output_file_created(self):
        # Ensure that the output file is not present initially
        self.assertFalse(os.path.exists(self.output_file_path))

        sorter = NumericStringSorter(self.input_file_path, self.output_file_path)
        sorter.execute()

        # Check if the output file is created after execution
        self.assertTrue(os.path.exists(self.output_file_path))

    def test_sort_and_compare_with_expected_output(self):
        # Input file with known data
        input_file_path = "../data/example-list.txt"
        # Expected output for the given input
        expected_output_path = "../data/sample-output.txt"

        with tempfile.NamedTemporaryFile(mode="w") as temp_output_file:
            sorter = NumericStringSorter(input_file_path, temp_output_file.name)
            sorter.execute()

            # Read sorted strings from the temporary output file
            with open(temp_output_file.name, "r") as file:
                sorted_strings = file.read().splitlines()

        # Read expected output from the provided file
        with open(expected_output_path, "r") as file:
            expected_sorted_strings = file.read().splitlines()

        # Compare the actual and expected sorted strings
        self.assertEqual(sorted_strings, expected_sorted_strings)

    def test_validate_file_exists_input_not_found(self):
        input_file_path = os.path.join(self.test_dir.name, "non_existent_file.txt")
        output_file_path = os.path.join(self.test_dir.name, "output.txt")

        with self.assertRaises(FileNotFoundError) as context:
            sorter = NumericStringSorter(input_file_path, output_file_path)
            sorter._validate_file_exists()

        expected_error_message = f"Input file not found: {input_file_path}"
        self.assertEqual(str(context.exception), expected_error_message)

    def test_validate_file_exists_output_directory_not_found(self):
        input_file_path = os.path.join(self.test_dir.name, "input.txt")
        output_file_path = os.path.join(
            self.test_dir.name, "non_existent_directory", "output.txt"
        )

        sorter = NumericStringSorter(input_file_path, output_file_path)
        sorter._validate_file_exists()

        # Check if the directory was created
        expected_output_directory = os.path.join(
            self.test_dir.name, "non_existent_directory"
        )
        self.assertTrue(os.path.exists(expected_output_directory))


if __name__ == "__main__":
    unittest.main()
