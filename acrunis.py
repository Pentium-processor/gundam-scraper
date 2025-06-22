import time 
def counter(start,end):
    numbers=[x for x in range(start,end+1,1)]
    for num in numbers:
        print(num,end='\r')
        time.sleep(0.1)
        
if __name__=="__main__":
    counter(1,100)