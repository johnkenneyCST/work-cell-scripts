
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

class PeptideHandler:
    def __init__(self, st_issues, config) -> None:
        self.st_numbers = st_issues
        self.config = config
        self.st_dict = {}
        self.makeRequest()

    def makeRequest(self):
        for i in range(len(self.st_numbers)):
            self.st_dict[self.st_numbers[i]] = []
        
        for i in self.st_numbers:
            try: 
                request = requests.get(url=self.config['barcode-retrieval']['jira-scpd-details-url-prod']+i)
            except Exception as e:
                exit(e)
            else:
                print(i)
                for j in request.json()['List']:
                    self.st_dict[i].append(ST_Issue_Entry(j['ID'], j["ISSUENUM"], j['MONOCLONALPROJECT'], j['ANIMAL'], 
                                                          j['NUMBEROFSAMPLES'], j['PEPTIDENAMES'],j['PLATEBARCODE'], 
                                                          j['EAPBARCODE'], j['PEPTIDERESERVOIR']))
                    


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

if __name__ == "__main__":
    args = parser.parse_args()
    st_issues = args.st_issues.split(" ")
    config = load_configs()
    pep_handler = PeptideHandler(st_issues, config)