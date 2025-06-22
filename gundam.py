from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
import requests
import os
import json
gundam_armors = [
    # Defensive & Specialized Armors
    "Luna Titanium Alloy",
    "Gundarium Alloy",
    "Phase Shift (PS) Armor",
    "Trans-Phase Armor",
    "Anti-Beam Coating / Anti-Beam Armor",
    "Electro-Magnetic Armor",

    # Transformation / Utility Armors
    "Variable Phase Shift Armor",
    "Armor Schneider / Modular Armor",
    "E-Carbon Armor",

    # Exotic / High-End Armors
    "Gundanium Alloy",
    "Nanolaminate Armor",
    "GN Field / GN Composite Armor",
    "I-Field & Beam Shielding",

    # Experimental / Conceptual Armors
    "Psycho-Frame",
    "Full Psycho-Frame",
    "VPS Armor",

    # Miscellaneous / Unique Armors
    "Reactive Armor",
    "Nano Skin / Self-Healing Armor",
    "ABC (Anti-Beam Coating) Mantle"
]

gundam_mechanical_designers = [
    "Akira Yasuda",
    "Hajime Katoki",
    "Hitoshi Fukuchi",
    "Ippei Gyoubu",
    "Junichi Akutsu",
    "Junya Ishigaki",
    "Kanetake Ebikawa",
    "Kazuhisa Kondo",
    "Kazumi Fujita",
    "Kenji Teraoka",
    "Kimitoshi Yamane",
    "Kyoshi Takigawa",
    "Mamoru Nagano",
    "Mika Akitaka",
    "Naohiro Washio",
    "Ikuto Yamashita",
    "Kunio Okawara",
    "Takayuki Yanase",
    "Yutaka Izubuchi",
    "Yuuichi Hasegawa",
    "Syd Mead",
    "JNTHED"
]
console=Console()
mech_info={}
url=console.input("[cyan][bold] URL:")
while url.startswith("https://gundam.fandom")!=True or len(url)>2000 or url.startswith("https://")!=True and len(url)>2000:
    console.print("Invalid url please try again")
    url=console.input("[red][bold] URL:")
else:
 payload={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"}
 r=requests.get(url,data=payload)
 if r.status_code==200:
    file_name="{html_file_name}.html".format(html_file_name=url[url.index("i/")+2:])
    with open(file=file_name,encoding="UTF-8",mode="a")as a:
       a.write(r.text)
    open_html_file=open(file_name,"r")
    info_extractor=BeautifulSoup(open_html_file,"html.parser")
    armanents=[]
    MS_name=info_extractor.title.string[:info_extractor.title.string.index("|")]
    for heading in info_extractor.find_all("dt"):
       armanents.append(heading.string)
    set_armanents=set(armanents)
    mech_info["Armanents"]=list(set_armanents)
    for ms_type in info_extractor.find_all("p"):
       white_space_remover=str(ms_type.string).strip()
       if white_space_remover.endswith("Mobile Suit")==True or white_space_remover.endswith("Mobile Fighter") or white_space_remover.endswith("Mobile Worker") or white_space_remover.endswith("Mobile Armor"):
          unit_type=white_space_remover
          mech_info["Unit Type"]=unit_type
          break

    for n in info_extractor.find_all("a"):
       s=str(n.string)
       if s.endswith("Reactor")==True or s.endswith("Drive")==True or s.endswith("Engine")==True or s.endswith("Tau")==True:
        power_reactor=s.strip()
        mech_info["Power Reactor"]=power_reactor
       else:
          for mech in gundam_mechanical_designers:
             if s==mech:
                mechanical_designer=s.strip()
                mech_info["Mechanical Designer"]=mechanical_designer
    else:
        for x in info_extractor.find_all("li"):
           if str(x.string).endswith("metric tons")==True:
              empty_weight=x.string
              mech_info["Empty Weight"]=empty_weight
           elif s.endswith("Reactor")==True or s.endswith("Drive")==True or s.endswith("Engine")==True or s.endswith("Tau")==True:
              power_reactor=s.strip()
              mech_info["Power Reactor"]=power_reactor
        for b in info_extractor.find_all("span"):
           if str(b.string).endswith("meters")==True:
              overall_height=b.string
              mech_info["Overall Height"]=overall_height
        dnx=[]
        for b in mech_info.keys():
           dnx.append(b)
        def create_table():
          table=Table(title=MS_name,title_style="bold cyan",style="cyan",title_justify="center")
          for key in mech_info.keys():
              if key not in dnx:
                 continue
              else:
                 table.add_column(key)
          dnx.clear()
          for ab in mech_info.values():
             dnx.append(str(ab))
          if len(dnx)==6:
             table.add_row(dnx[0],dnx[1],dnx[2],dnx[3],dnx[4],dnx[5])
          elif len(dnx)==5:
             table.add_row(dnx[0],dnx[1],dnx[2],dnx[3],dnx[4])
          elif len(dnx)==4:
             table.add_row(dnx[0],dnx[1],dnx[2],dnx[3])
          elif len(dnx)==3:
             table.add_row(dnx[0],dnx[1],dnx[2])
          elif len(dnx)==2:
             table.add_row(dnx[0],dnx[1])
          elif len(dnx)==1:
             table.add_row(dnx[0])
          console.print(table)

        create_table()
        if os.path.exists(file_name)==True:
           os.remove(file_name)
           with open("mech.json","a")as a:
                json_data=json.dumps(mech_info,indent=4,sort_keys=True,separators={",",":"})
                a.write(json_data)
 else:
    quit(console.print("[red][bold] You are not permitted to extract data from this webpage."))
