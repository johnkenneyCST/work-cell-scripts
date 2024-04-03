import requests
import sys
import yaml

def makeRequest():
    try:
        with open("./config/config.yaml") as file:
            configs = yaml.safe_load(file)
    except Exception as e:
        exit(e)
    
    req = requests.get(url=configs['barcode-retrieval']['jira-scpd-details-url-dev04']+"ST-705")
    # for k, v in req.json().items():
    #     for i in v:
    #         print("\n",i["ID"])
    #         for kk, vv in i.items():
    #             print(f"\t{kk, vv}")

    for key, value in req.json().items():
        for items in value:
            ST_Issue_Entry(id=items["ID"], 
                           issue_num=items["ISSUENUM"], 
                           mono_proj_num=items["MONOCLONALPROJECT"],
                           animal_num=items["ANIMAL"],
                           num_of_samples=items["NUMBEROFSAMPLES"],
                           peptide_names=items["PEPTIDENAMES"],
                           tfw_barcode=items["PLATEBARCODE"],
                           eap_barcode=items["EAPBARCODE"],
                           peptide_reservoir=items["PEPTIDERESERVOIR"] or "")

            



class ST_Issue_Entry:
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



if __name__ == "__main__":
    makeRequest()


