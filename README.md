# email-analyzer

usage: Email Analyzer [-h] [-i INPUT_DIRECTORY] [-n NAME]
                      [-o OUTPUT_DIRECTORY] [-c] [-s] [-p]

A script to analyze your email inbox and sort by number of emails from an
address or total_size of emails from address

options:
  -h, --help            show this help message and exit
  -i INPUT_DIRECTORY, --input_directory INPUT_DIRECTORY
                        directory containing EML files. Required on first run
  -n NAME, --name NAME  name of output file. Default is ea_output
  -o OUTPUT_DIRECTORY, --output_directory OUTPUT_DIRECTORY
                        directory to output files to. Default is output/
  -c, --count           output a separate file sorted by email count per email
                        address
  -s, --size            output a separate file sorted by total size of emails
                        per email address
  -p, --process         process eml files. True on first run

Pre-alpha
