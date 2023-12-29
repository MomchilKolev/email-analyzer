import json
import os
import re
from datetime import datetime


class EmailAnalyzer:
    def __init__(self, **kwargs):
        """Init EmailAnalyzer, take command line arguments as kwargs"""
        # self.regex_pattern = re.compile(
        #     r"From: "'"'r"([A-Za-z0-9]+( [A-Za-z0-9]+)+)"'"'r" <[-A-Za-z0-9!#$%&'*+/=?^_`{|}~]+(?:\.[-A-Za-z0-9!#$%&'*+/=?^_`{|}~]+)*@(?:[A-Za-z0-9](?:[-A-Za-z0-9]*[A-Za-z0-9])?\.)+[A-Za-z0-9](?:[-A-Za-z0-9]*[A-Za-z0-9])?>",
        #     re.IGNORECASE)
        self.regex_pattern = re.compile(r"From: "'"'r".*"'"'r" <.*>", re.IGNORECASE)
        self.emails = {}

        self.input_dir = kwargs['input_directory']
        self.name = kwargs['name'] or 'ea_output'
        self.count = kwargs['count']
        self.output_dir = kwargs['output_directory'] or 'output'
        self.size = kwargs['size']
        self.process = kwargs['process']

        if not self.input_dir:
            raise ValueError("-i <input_directory> required")

        # Process emails and save to json
        if not os.path.isdir(self.output_dir) or os.path.isdir(self.output_dir) and self.process:
            self.process_emails()

        # Sort descending count
        if self.count:
            self.sorted_list(sort_by="count", name=self.name)

        # Sort descending total_size
        if self.size:
            self.sorted_list(sort_by="total_size_in_mb", name=self.name)

    def process_emails(self):
        """Process emails and save to output_directory"""
        path = self.input_dir
        output_dir = self.output_dir
        start_time = datetime.now()

        # Walk through and add name, email from each to output
        for root, dirs, files in os.walk(path):
            for file in files:
                with open(os.path.join(root, file)) as data_file:
                    file_size = os.path.getsize(os.path.join(root, file)) >> 20 # convert to MB
                    [self.add_email(line, file_size) for line in data_file.readlines() if
                     re.search(self.regex_pattern, line)]
        time_elapsed = (datetime.now() - start_time).seconds

        # If output directory does not exist, create it
        if not os.path.isdir(self.output_dir):
            os.mkdir(output_dir)

        # Save output file
        try:
            with open(f"{output_dir}/{self.name}.json", "w") as outfile:
                json.dump(self.emails, outfile)
        except FileNotFoundError as error_message:
            print(f"Error: {error_message}")
        else:
            print(f"Completed in {time_elapsed}")

    def add_email(self, email_string, file_size):
        """Add email to output, but adding to count and total_size for this email address"""
        pattern = re.compile(r"^.*From: \"(.*)\" <(.*)>")
        matches = [match for match in re.split(pattern, email_string.strip()) if match]
        name, email = [match for match in re.split(pattern, email_string.strip()) if match]
        if len(matches) > 2:
            print(matches)
        try:
            self.emails[email]["count"] += 1
            self.emails[email]["total_size_in_mb"] += file_size
        except BaseException as error:
            # print("error", error)
            self.emails[email] = {"count": 1, "total_size_in_mb": file_size}
        # finally:
        # print(f"current email dict: {self.emails}")

    def sorted_list(self, sort_by, name):
        """Create sorted list and save file"""
        name = name or "ea_output"
        if sort_by != "count" and sort_by != "total_size_in_mb":
            raise ValueError("sort_by should be either count or total_size")
        with open("email_analyzer_output.json", "r") as data_file:
            json_file = data_file.read()
            json_data = list(json.loads(json_file).items())
            json_data.sort(reverse=True, key=lambda item: item[1][sort_by])
            with open(f"{self.output_dir}/{name}_sorted_by_{sort_by}.json", "w") as outfile:
                json.dump(json_data, outfile)
