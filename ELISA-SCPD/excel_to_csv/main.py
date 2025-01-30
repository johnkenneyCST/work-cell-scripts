import argparse
import openpyxl
import pandas as pd
import os
# python ELISA-SCPD/excel_to_csv/main.py --files "C:\Users\Biosero\Desktop\SCPD-ELISA-Day-2-Plate-Reader-Files\SCPD_ELISA_EAP985.xlsx, C:\Users\Biosero\Desktop\SCPD-ELISA-Day-2-Plate-Reader-Files\SCPD_ELISA_EAP986.xlsx"

parser = argparse.ArgumentParser()
parser.add_argument('--files', type=str, required=True)
args = parser.parse_args()

OUTPUT_DIR = "C:/Users/Biosero/Desktop/SCPD-ELISA-Day-2-Plate-Reader-Files/csv_files/"



def excel_to_csv(excel, new_file_path):
    tmp = excel.split("\\")[-1]
    old_file_name = tmp.split(".")[0]
    try:
        df = pd.read_excel(excel, engine="openpyxl")
        df.rename(columns={"Unnamed: 1": '', "Unnamed: 2": ''}, inplace=True)
        df.to_csv(f"{OUTPUT_DIR}{old_file_name}.csv", index=False)    
    except Exception as e:
        exit(e)



if __name__ == "__main__":
    files = args.files.split(",")
    files = [i.replace(" ", "") for i in files]

    for i in files:
        excel_to_csv(i, OUTPUT_DIR)