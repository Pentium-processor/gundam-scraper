from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
import os
from read_file import file_content_reader
from save import save_ms_data
import time
import subprocess

open_txt_file=open("mechanical_designers.txt","r")
def remove_whitespace(text):
    z=lambda string:string.strip()
    return z(text)

designers=list(map(remove_whitespace,open_txt_file.readlines()))

console=Console()
mech_info={}
if os.path.exists("MS_DATA")==False:
  subprocess.run("mkdir MS_DATA")
else:
  mobile_suit=console.input("[green] do you want to see the information of a mobile suit you searched up before?:")
  if mobile_suit in ["y","Y"]:
      file_content_reader()
  else:

    quit_program_input=console.input("[red][bold] do you wish to quit the program?:")
    if quit_program_input in ["y","Y"]:
       subprocess.run("clear")
       quit("")
    elif quit_program_input in ["n","N"]:
      command = "cat mobile_suit.txt | fzf"
      ms_name=str(subprocess.check_output(command,shell=True,text=True)).strip()
      url="https://gundam.fandom.com/wiki/"+"_".join(ms_name.split())
      print(url)
      raw_html_source_code=subprocess.run(f"lynx {url} -source -accept_all_cookies",capture_output=True,shell=True,text=True)
      time.sleep(5)
      for char in ms_name:
        if char=="/":
           ms_name=ms_name.replace(char,"")
        else:
           continue

      file_name="{html_file_name}.html".format(html_file_name="_".join(ms_name.split()))
      with open(file=file_name,encoding="UTF-8",mode="w")as a:
       a.write(str(raw_html_source_code.stdout))

      open_html_file=open(file_name,"r",encoding="UTF-8")
      info_extractor=BeautifulSoup(open_html_file,"html.parser")
      armanents=[]
      for heading in info_extractor.find_all("dt"):
          if str(heading.string).endswith(("Form","Type","Series","Games","Manga","Movies","ONAs",str(None))) == True:
             continue
          else:
           armanents.append(heading.string)

      set_armanents=set(armanents)
      mech_info["Armaments"]=list(set_armanents)
      for ms_type in info_extractor.find_all("p"):
       white_space_remover=str(ms_type.string).strip()
       if white_space_remover.endswith(("Suit","Fighter","Worker","Armor","Weapon","Craft")) == True:
          unit_type=white_space_remover
          mech_info["Unit Type"]=unit_type
          break

      for n in info_extractor.find_all("a"):
       s=str(n.string)
       if s.endswith(("Reactor","Engine","Drive","Tau")):
        power_reactor=s.strip()
        mech_info["Power Reactor"]=power_reactor

       elif s.strip() in designers:
           mech_info["Mechanical Designer"] = s.strip()
      for x in info_extractor.find_all("li"):
           if str(x.string).endswith("metric tons")==True:
              empty_weight=x.string
              mech_info["Empty Weight"]=empty_weight
           for b in info_extractor.find_all("span"):
            if str(b.string).endswith("meters")==True  and float(str(b.string)[:str(b.string).index(" ")])<100:
              overall_height=b.string
              mech_info["Height"]=overall_height
      dnx=[]
      for b in mech_info.keys():
          dnx.append(b)
      def create_table():
          table=Table(title=ms_name,title_style="bold cyan",style="cyan",title_justify="center")
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
      save_ms_data_opt=console.input(f"[blue][bold] do you wish to save {ms_name}\'s mobile suit data y/n: ")
      for filename in os.listdir():
       if filename.endswith(".html"):
            subprocess.run(["rm","-r",filename])
       else:
            continue


      if save_ms_data_opt=="y" or save_ms_data_opt=="Y":
         mech_info["ms_name"]=ms_name
         save_ms_data(file_name=f"{file_name[:file_name.index('.html')]}.json",mech_stats=mech_info)
      else:
          pass
