import argparse

from string_sorter.numeric_string_sorter import NumericStringSorter


def parse_args():
    parser = argparse.ArgumentParser(
        description="Sort strings from an input file and write the result to an output file."
    )
    parser.add_argument("input_file", help="Path to the input file")
    parser.add_argument("output_file", help="Path to the output file")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    sorter = NumericStringSorter(args.input_file, args.output_file)
    sorter.execute()
