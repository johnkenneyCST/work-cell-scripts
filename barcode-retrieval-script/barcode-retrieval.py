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
        # print(key, value)
        for items in value:
            # print(type(items))
            print("\n")
            ST_Issue_Entry(id=items["ID"])
            



class ST_Issue_Entry:
    def __init__(self, 
                 id,
                 issue_num,
                 mono_proj_num,
                 animal_num,
                 num_of_of_samples,
                 tfw_barcode,
                 eap_barcode,
                 peptide_reservoir) -> None:
        
        self.id = id
        self.issue_num = issue_num
        self.mono_proj_num = mono_proj_num 
        self.animal_num

if __name__ == "__main__":
    makeRequest()


