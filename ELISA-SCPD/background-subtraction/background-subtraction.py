import argparse
import csv 
import openpyxl 
from openpyxl import load_workbook
from openpyxl.styles import Font, Border, Side
import pandas as pd
import re

parser = argparse.ArgumentParser(prog="background-subtraction.py")
parser.add_argument('--files', type=str, required=True)
args = parser.parse_args()

# These columns are the columns where the degen peptides will be
DEGEN_PEPTIDE_COLS = ["21","22","23"]

# These are the columns where the regular peptides will go
REG_PEPTIDE_COLS = ["1","2","3",
                    "5", "6","7",
                    "9","10","11",
                    "13","14","15",
                    "17","18","19"]

# These are the rows where all peptides will go 
PEPTIDE_ROWS = ["A","C","E","G","I","K","M","O"]

PEPTIDE_GROUPS = {1:["1","2","3"],
                  2: ["5", "6","7"],
                  3: ["9","10","11"],
                  4:["13","14","15"],
                  5: ["17","18","19"]}

class file_handler:
    def __init__(self, file) -> None:
        self.file = file
        self.read_file()

    def read_file(self):
        self.meta_data = pd.read_excel(self.file, engine='openpyxl')

        barcodes = self.meta_data[self.meta_data['Unnamed: 1'].str.contains("EAP", na=False)]
        barcode_list = barcodes['Unnamed: 1'].tolist()
        index_list = barcodes["Unnamed: 1"].index.tolist()
        self.plate_list = {}
        for i in range(len(barcode_list)):
            self.plate_list[f"{barcode_list[i]}"] = self.plate(file_intance=self,barcode=barcode_list[i], start_index=index_list[i])
        

        self.meta_data.rename(columns={"Unnamed: 1": '', "Unnamed: 2": ''}, inplace=True)
        self.meta_data.to_excel(self.file, engine="openpyxl", index=False)
        self.workbook = load_workbook(self.file)
        self.worksheet = self.workbook.active
        no_border = Border(left=Side(border_style=None),
                                     right=Side(border_style=None),
                                     top=Side(border_style=None),
                                     bottom=Side(border_style=None))
        for cell in self.worksheet[1]:
            cell.font = Font(bold=False)
            cell.border = no_border
        self.workbook.save(self.file)

    class plate:
        def __init__(self, file_intance, barcode, start_index) -> None:
            self.file_handler = file_intance
            self.barcode = barcode
            self.start_index = start_index + 4  
            self.collect_wells()
            self.subtract_degen()
            self.overwriteFile()
            

        def collect_wells(self):
            self.wells = self.file_handler.meta_data[self.start_index:self.start_index+384]
            self.wells_list = self.wells["Unnamed: 1"].tolist()
            self.wells_list_data = self.wells["Unnamed: 2"].tolist()
            
            self.well_data_list = []
            self.index_counter = self.start_index
            for i in range(len(self.wells_list)):
                self.well_data_list.append(self.well(self, self.wells_list[i], self.wells_list_data[i], self.index_counter))
                self.index_counter += 1
        
        def subtract_degen(self):
            self.normal_peptides = []
            self.degen_peptides = {}
            for i in self.well_data_list:
                if i.is_degen:
                    self.degen_peptides[i.well] = i
                elif i.is_reg_peptide:
                    self.normal_peptides.append(i)
                else:
                    continue
            
            for i in self.normal_peptides:
                i.new_value = round(i.value - self.degen_peptides[i.degen_peptide_to_sub].value, 4)

        def overwriteFile(self):
            for i in self.normal_peptides:
                self.file_handler.meta_data.loc[ i.index,"Unnamed: 2"] = i.new_value

        
        class well:
            def __init__(self, plate_instance, well, value, index) -> None:
                self.plate_instance = plate_instance
                self.well = well 
                self.value = value
                self.is_degen = False
                self.is_reg_peptide = False
                self.new_value = None
                self.index = index

                self.determine_if_degen()
                self.determine_if_regular_peptide()

                if self.is_reg_peptide:
                    self.find_corresponding_degen_peptide()

            def determine_if_degen(self):
                # This function will determine whether this well is a degenerate peptide well, since the location of the degen peptide will always reside in the same cols and rows we can calculate this

                tmpRowLetter = self.well[:1]
                tmpColNumber = self.well[1:]
                
                if tmpRowLetter in PEPTIDE_ROWS and tmpColNumber in DEGEN_PEPTIDE_COLS:
                    self.is_degen = True

            def determine_if_regular_peptide(self):
                tmpRowLetter = self.well[:1]
                tmpColNumber = self.well[1:]
                
                if tmpRowLetter in PEPTIDE_ROWS and tmpColNumber not in DEGEN_PEPTIDE_COLS and tmpColNumber in REG_PEPTIDE_COLS:
                    self.is_reg_peptide = True

            def find_corresponding_degen_peptide(self):
                # This function will be called if a peptide is not a degen, this will find the degen peptide to be subtracted from. 
                tmpColNumber = int(self.well[1:])
                for k, v in PEPTIDE_GROUPS.items():
                    if str(tmpColNumber) in v:
                        self.degen_peptide_index = v.index(str(tmpColNumber))
                        self.degen_peptide_to_sub = f"{self.well[:1]}{DEGEN_PEPTIDE_COLS[self.degen_peptide_index]}"


if __name__ == "__main__":
    files = args.files.split(",")
    files = [i.replace(" ", "") for i in files]
    for i in files:
        file_handler(i)