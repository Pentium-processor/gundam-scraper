from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
import requests
import os
import json
open_txt_file=open("mechanical_designers.txt","r")
console=Console()
current_dir=os.getcwd()
mech_info={}
def file_content_reader():
         console.print("[bold][green]Mobile gundam list:\n\t")
         if os.listdir()==[]:
            print("You have no log files about any mobile suit in the directory gundam_txt_files.")
         else:
          for index,name in enumerate(os.listdir(),start=1):
            print(f'{index}. {name}')
          enter_file=input("file name:")
          if os.path.exists(enter_file)==True:
           read_txt_file=open(enter_file,"r")
           os.system("clear")
           for text in read_txt_file.readlines():
               print("".join(text))
          else:
           console.print("[red][bold] file does not exist")

if os.path.exists("gundam_logs")==False:
  os.mkdir("gundam_logs")
elif os.path.exists("gundam_logs")==True:
  mobile_suit=console.input("[green] do you want to see the information of a mobile suit you searched up before?:")
  if mobile_suit=="y":
   os.chdir("gundam_logs")
   file_content_reader()
  else:
    quit_program_input=console.input("[red][bold] do you wish to quit the program?:")
    if quit_program_input=="y" or quit_program_input=="Y":
       os.system("clear")
       quit("")
    elif quit_program_input=="n" or quit_program_input=="N":
      mech_name=console.input("[cyan][bold] MOBILE SUIT NAME:")
      payload={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"}
      r=requests.get("https://gundam.fandom.com/wiki/"+mech_name,headers=payload)
      print(r.url)
      print(r.status_code)
      if r.status_code==200:
       file_name="{html_file_name}.html".format(html_file_name=mech_name)
      else:
       quit(console.print("[red][bold] You are not permitted to extract data from this webpage."))
      with open(file=file_name,encoding="UTF-8",mode="a")as a:
       a.write(r.text)
      open_html_file=open(file_name,"r",encoding="UTF-8")
      info_extractor=BeautifulSoup(open_html_file,"html.parser")
      armanents=[]
      MS_name=info_extractor.title.string[:info_extractor.title.string.index("|")]
      for heading in info_extractor.find_all("dt"):
        if str(heading.string).endswith("Form")==True or heading.string==None or str(heading.string).endswith("Type")==True or heading.string=="Television Series" or heading.string=="OVAs and ONAs" or heading.string=="Games" or heading.string=="Manga" or heading.string=="Movies":
             continue
        else:
          armanents.append(heading.string)

      set_armanents=set(armanents)
      mech_info["Armaments"]=list(set_armanents)
      for ms_type in info_extractor.find_all("p"):
       white_space_remover=str(ms_type.string).strip()
       if white_space_remover.endswith("Mobile Suit")==True or white_space_remover.endswith("Mobile Fighter") or white_space_remover.endswith("Mobile Worker") or white_space_remover.endswith("Mobile Armor") or white_space_remover.endswith("Weapon") or white_space_remover.endswith("Craft"):
          unit_type=white_space_remover
          mech_info["Unit Type"]=unit_type
          break

      for n in info_extractor.find_all("a"):
       s=str(n.string)
       if s.endswith("Reactor")==True or s.endswith("Drive")==True or s.endswith("Engine")==True or s.endswith("Tau")==True:
        power_reactor=s.strip()
        mech_info["Power Reactor"]=power_reactor
       else:
         for mech in open_txt_file.readlines():
            if s==mech:
             mechanical_designer=s.strip()
             mech_info["Mechanical Designer"]=mechanical_designer
      for x in info_extractor.find_all("li"):
           if str(x.string).endswith("metric tons")==True:
              empty_weight=x.string
              mech_info["Empty Weight"]=empty_weight
           for b in info_extractor.find_all("span"):
            if str(b.string).endswith("meters")==True and float(b.string[:b.string.index("meters")]) in range(15,21,1):
              overall_height=b.string
              mech_info["Overall Height"]=overall_height
      mech_info["Desc"]="".join(info_extractor.get_text()[info_extractor.get_text().index("Technology & Combat Characteristics[]")+len("Technology & Combat Characteristics[]"):info_extractor.get_text().index("Armaments[]")])
      dnx=[]
      print(mech_info)
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
          elif len(dnx)==7:
             table.add_row(dnx[0],dnx[1],dnx[2],dnx[3],dnx[4],dnx[5],dnx[6])
          elif len(dnx)==8:
             table.add_row(dnx[0],dnx[1],dnx[2],dnx[3],dnx[4],dnx[5],dnx[6])
          console.print(table)

      create_table()
      open_html_file.close()
      save_ms_data=console.input(f"[blue][bold] do you wish to save {MS_name}\'s mobile suit data y/n: ")
      for filename in os.listdir():
       if filename.endswith(".html"):
            os.remove(filename)
       else:
            continue


      if save_ms_data=="y" or save_ms_data=="Y":
         os.chdir("gundam_logs")
         with open(f"{file_name[:file_name.index('.html')]}.json","w") as a:
           mech_info["ms_name"]=MS_name
           del mech_info["Desc"]
           json.dump(mech_info,a,indent=4,separators=(":",","),sort_keys=True)
      else:
         pass
