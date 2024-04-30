"""
Author: John Kenney
Description: This script is the labware validation script for day 1 of the SCPD ELISA Work cell process. 
Labware for day 1:
- 384 
- 12 channels 
- 24 deep well

This script will live on the work cell PC and be called from within GBG.

"""

import requests
import sys
import yaml
import argparse
import os
import pandas as pd

# Arguments #
parser = argparse.ArgumentParser(prog="barcode-retrieval.py")
parser.add_argument("--st_issues", type=str, required=True)
parser.add_argument("--labware_file", type=str, required=True)
parser.add_argument("--validation_day", type=int, required=True, choices=[1,2])
args = parser.parse_args()
st_issues = args.st_issues.split(" ")
# test cmd line: python barcode-retrieval-script/barcode-retrieval.py --st_issues "ST-797 ST-796" --labware_file "C:\Users\jkenney\Downloads\test-carousel.csv"
# test cmd line: python ELISA-SCPD/labware-validation-script/labware-validation.py --st_issues "ST-797 ST-796" --labware_file "C:\Users\jkenney\Downloads\test-carousel.csv"
st_issues_dict = {}

def makeRequest():
    """
    This function will utilize the JIRA-SCPD-Request API and retrieve/return the TGE information in a given ST issue. 
    It will also create ST_Issue_Entry instances for each row in a given ST issue. 
    
    """
    for i in range(len(st_issues)):
        st_issues_dict[st_issues[i]] = []
    try:
        with open("C:/Users/Biosero/Desktop/work-cell-scripts/config/config.yaml") as file:
            configs = yaml.safe_load(file)
    except Exception as e:
        sys.exit(e)
    for st_iss in st_issues:
        req = requests.get(url=configs['barcode-retrieval']['jira-scpd-details-url-prod']+st_iss)
        for key, value in req.json().items():
            for items in value:
                st_issues_dict[st_iss].append(ST_Issue_Entry(id=items["ID"], 
                            issue_num=items["ISSUENUM"], 
                            mono_proj_num=items["MONOCLONALPROJECT"],
                            animal_num=items["ANIMAL"],
                            num_of_samples=items["NUMBEROFSAMPLES"],
                            peptide_names=items["PEPTIDENAMES"],
                            tfw_barcode=items["PLATEBARCODE"],
                            eap_barcode=items["EAPBARCODE"],
                            peptide_reservoir=items["PEPTIDERESERVOIR"] or ""))

def parse_labware_file():
    df = pd.read_csv(args.labware_file)
    labware_on_workcell = df["Barcode"].values.tolist()
    return labware_on_workcell

def make_labware_list_from_jira():
    tmpList = []
    for key, value in st_issues_dict.items():
        for tge_row in value:
            tmpList.append(tge_row.eap_barcode)
            if args.validation_day == 1:
                tmpList.append(tge_row.peptide_reservoir_barcode)
            elif args.validation_day == 2:
                tmpList.append(tge_row.tfw_barcode)
    return tmpList

class ST_Issue_Entry:
    """ 
    This class is for storing the TGE information from JIRA. A user is given a set of ST numbers, using the API we get those numbers and the data is passed 
    to this class. 

    Each instance of this class represents a single row in the TGE.
    """
    def __init__(self, 
                 id,
                 issue_num,
                 mono_proj_num,
                 animal_num,
                 num_of_samples,
                 peptide_names,
                 tfw_barcode,
                 eap_barcode,
                 peptide_reservoir) -> None:
        
        self.id = id
        self.issue_num = issue_num
        self.mono_proj_num = mono_proj_num.split(" ")[0]
        self.animal_num = animal_num
        self.num_of_samples = num_of_samples
        self.peptide_names = peptide_names.split("<")[0].strip()
        self.tfw_barcode = tfw_barcode
        self.eap_barcode = eap_barcode
        self.peptide_reservoir_barcode = peptide_reservoir

        # print(f"""id: {self.id}\n\tissue num: {self.issue_num}\n\tmono project num: {self.mono_proj_num}\n\t
        # animal num: {self.animal_num}\n\tnum samples: {self.num_of_samples}\n\tpeptide names {self.peptide_names}
        # \n\ttfw barcode {self.tfw_barcode}\n\teap barcode: {self.eap_barcode}\n\tpeptide reservoir barcode: {self.peptide_reservoir_barcode}""")

def compare_list():
    final_list = list(set(work_cell_barcodes) - set(jira_barcodes))
    if len(final_list) != 0:
        print("Discrepency in lists")
        print(final_list)
        sys.exit(400)
    else:
        print("Labware Validated !")
        sys.exit(200)

if __name__ == "__main__":
    makeRequest()
    work_cell_barcodes = parse_labware_file()

    jira_barcodes = make_labware_list_from_jira()
    print(jira_barcodes)
    compare_list()
    

