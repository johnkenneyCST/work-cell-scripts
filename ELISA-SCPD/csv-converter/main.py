import argparse
import csv
import pandas as pd
import os


parser = argparse.ArgumentParser()
parser.add_argument('--file', required=True)
args = parser.parse_args()
if __name__ == "__main__":
    df = pd.read_excel(args.file)
    df.to_csv(f"{os.getcwd()}/test.csv", index=False)