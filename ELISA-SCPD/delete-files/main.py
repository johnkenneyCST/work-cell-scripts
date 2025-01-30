import argparse
import openpyxl
import pandas as pd
import os
# python ELISA-SCPD/delete-files/main.py --files "C:\Users\Biosero\Desktop\SCPD-ELISA-Day-2-Plate-Reader-Files\SCPD_ELISA_EAP985.xlsx, C:\Users\Biosero\Desktop\SCPD-ELISA-Day-2-Plate-Reader-Files\SCPD_ELISA_EAP986.xlsx"

parser = argparse.ArgumentParser()
parser.add_argument('--files', type=str, required=True)
args = parser.parse_args()


def delete_file(file):
    os.remove(file)



if __name__ == "__main__":
    files = args.files.split(",")
    files = [i.replace(" ", "") for i in files]

    for i in files:
        delete_file(i)