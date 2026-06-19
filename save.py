import json
from os import chdir
def save_ms_data(file_name,mech_stats):
    chdir("MS_DATA")
    with open(file_name,"w")as json_data:
     json.dump(mech_stats,json_data,indent=4,separators=(",",":"),sort_keys=True)
    chdir("..")
