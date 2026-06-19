from os import chdir,listdir
def file_content_reader():
         chdir("MS_DATA")
         print("Mobile gundam list:\n\t")
         if listdir()==[]:
            print("You have no log files about any mobile suit in the directory MS_DATA.")
         else:
          for index,name in enumerate(listdir(),start=1):
             print(f'{index}. {name}')

          enter_file=input("file name:")
          if enter_file in listdir():
           txt_file=open(enter_file,"r")
           print("".join(txt_file.readlines()))
          else:
           print("File does not exist")
