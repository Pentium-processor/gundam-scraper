from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
import requests
import os
import platform
numbers=[x for x in range(15,20,1)]
strnumbers=[]
for n in numbers:
    strnumbers.append(str(n))
console=Console()
current_dir=os.getcwd()
mech_info={}
mechanical_designers=[]
def clear_screen():
   if str(platform.platform()).startswith("Linux")==True:
      os.system("clear")
   else:
      os.system("cls")

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
           clear_screen()
           for text in read_txt_file.readlines():
               print("".join(text))
          else:
           console.print("[red][bold] file does not exist")
capital_letters=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
if os.path.exists("gundam_txt_files")==False:
  os.mkdir("gundam_txt_files")
elif os.path.exists("gundam_txt_files")==True:
  mobile_suit=console.input("[green] do you want to see the information of a mobile suit you searched up before?:")
  if mobile_suit=="y":
   os.chdir("gundam_txt_files")
   file_content_reader()
  else:
    quit_program_input=console.input("[red][bold] do you wish to quit the program?:")
    if quit_program_input=="y" or quit_program_input=="Y":
       clear_screen()
       quit("")
    elif quit_program_input=="n" or quit_program_input=="N":
      url=console.input("[cyan][bold] URL:")
      while url.startswith("https://gundam.fandom")!=True or len(url)>2000 or url.startswith("https://")!=True and len(url)>2000:
       console.print("Invalid url please try again")
       url=console.input("[red][bold] URL:")
      else:
       payload={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"}
       r=requests.get(url,data=payload)
      if os.path.exists("mech_designers.html")!=True:
       os.chdir(current_dir)
      with open("mech_designers.html","a",encoding="UTF-8")as mech_design:
        response=requests.get("https://gundam.fandom.com/wiki/Category:Mechanical_Designers")
        mech_design.write(str(response.text))

      if r.status_code==200:
       file_name="{html_file_name}.html".format(html_file_name=url[url.index("i/")+2:])
      else:
       quit(console.print("[red][bold] You are not permitted to extract data from this webpage."))
      with open(file=file_name,encoding="UTF-8",mode="a")as a:
       a.write(r.text)
      open_html_file=open(file_name,"r",encoding="UTF-8")
      open_mech_designer_file=open("mech_designers.html","r",encoding="UTF-8")
      mechanical_designer_extractor=BeautifulSoup(open_mech_designer_file,"html.parser")
      info_extractor=BeautifulSoup(open_html_file,"html.parser")
      for n in mechanical_designer_extractor.find_all("a"):
       for letter in capital_letters:
         if str(n.string).startswith(letter)==True and " " in str(n.string):
           mechanical_designers.append(n.string)
      else:
       del mechanical_designers[0]
      mechanical_designers.append("Kaneko Tsukasa")
      set_of_mechanical_designers=set(mechanical_designers)
      convert_to_list=list(set_of_mechanical_designers)
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
          for mech in convert_to_list:
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
           if str(b.string).endswith("meters")==True and float(b.string[:b.string.index("meters")]) in range(15,21,1):
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
        open_html_file.close()
        save_ms_data=console.input(f"[blue][bold] do you wish to save {MS_name}\'s mobile suit data y/n: ")
        for filename in os.listdir():
         if filename.endswith(".html"):
               os.remove(filename)
         else:
                continue

        if save_ms_data=="y" or save_ms_data=="Y":
         os.chdir("gundam_txt_files")
         with open(f"{file_name}.txt","a") as a:
          a.write("Model Name - "+MS_name+"\n")
          for key,value in mech_info.items():
             a.write("{d} - {e}".format(d=key,e=value)+"\n")
        else:
          pass
