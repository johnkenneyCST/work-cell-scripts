
import pandas as pd
import csv
import argparse
import requests
import io
import os
import yaml

parser = argparse.ArgumentParser(prog='peptide-link.py',
                                 description="This script will be triggered by the work cell after a plate reader file has been generated. It will link the peptide data to the reader data")

parser.add_argument("--st_issues", type=str, required=True)
parser.add_argument('--file', type=argparse.FileType('r'), required=True, help="The output file from the epoch 2 on the workcell")

def load_configs():
    try:
        with open("./config/config.yaml") as file:
            configs = yaml.safe_load(file)
    except Exception as e:
        exit(e)
    else:
         return configs



if __name__ == "__main__":
    args = parser.parse_args()
    config = load_configs()
