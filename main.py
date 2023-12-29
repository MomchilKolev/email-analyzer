import argparse

from email_analyzer import EmailAnalyzer

# Initialize parser
parser = argparse.ArgumentParser(
    prog="Email Analyzer",
    description="A script to analyze your email inbox and sort by number of emails from an "
                "address or total_size of emails from address",
    epilog="Pre-alpha"
)

# Arguments
parser.add_argument("-i", "--input_directory", help="directory containing EML files. Required on "
                                                    "first run")
parser.add_argument("-n", "--name", help="name of output file. Default is ea_output",
                    default="ea_output")
parser.add_argument("-o", "--output_directory", help="directory to output files to. Default is "
                                                     "output/",
                    default="output")
parser.add_argument("-c", "--count", action="store_true", help="output a separate file "
                                                               "sorted by email "
                                                               "count "
                                                               "per email address")
parser.add_argument("-s", "--size", action="store_true",
                    help="output a separate file sorted by total size of emails per "
                         "email address")
parser.add_argument('-p', '--process', action="store_true", help="process eml files. True on "
                                                                 "first run")

args = parser.parse_args()

# print("args", args)
email_analyzer = EmailAnalyzer(**vars(args))
