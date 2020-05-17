import pandas as pd
import os
from glob import glob 
import re

#debug full print options
#pd.set_option('display.max_rows', -1)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

#fixed width formatting lambdas
myl1=lambda x:  ' '*(6-len(str(x)))+str(x)
myl2=lambda x:  ' '*(11-len(str(x)))+str(x)
myl3=lambda x:  ' '*(10-len(str(x)))+str(x)
myl4=lambda x:  ' '*(8-len(str(x)))+str(x)
myl5=lambda x:  ' '*(3-len(str(x)))+str(x)
myl6=lambda x:  ' '*(5-len(str(x)))+str(x)

srcpath='/Users/nickvancise/Desktop/avaps'

def tail(f, n=1, bs=1024):
    f.seek(0,2)
    l = 1-f.read(1).count('\n')
    B = f.tell()
    while n >= l and B > 0:
            block = min(bs, B)
            B -= block
            f.seek(B, 0)
            l += f.read(block).count('\n')
    f.seek(B, 0)
    l = min(l,n)
    lines = f.readlines()[-l:]
    f.close()
    return lines


#header format..
#header='''AVAPS-T01 STA 132855101 140630 171042.59
#AVAPS-T01 COM            UTC     UTC      Wind   Vert      GPS        GPS     Geopoten GPS Wind    GPS   
#AVAPS-T01 COM   Sonde    Date    Time     Spd    Veloc  Longitude   Latitude  Altitude Snd Error Altitude
#AVAPS-T01 COM    ID     yymmdd hhmmss.ss  (m/s)  (m/s)    (deg)       (deg)      (m)   Sat (m/s)    (m)  
#AVAPS-T01 COM --------- ------ --------- ------ ------ ----------- ---------- -------- --- ----- --------\n'''


def processfile(file):
	headertmp=''
		
	with open(file) as f:
		Lines = f.readlines() 
	  
		count = 0
		# Strips the newline character 
		for line in Lines: 
			if count==0:
				headertmp+=line
			else:
				headertmp+=line[0:40]+line[69:116]+line[134:154]
			count+=1
			if count==5:break;

	with open(file) as f:
		footer=tail(f,19)


	df=pd.read_fwf(file,header=None,colspecs=[(0,13),(14,23),(24,30),(31,40),(70,76),(77,83),(84,95),(96,106),(107,116),(134,138),(138,144),(144,154)],dtype=str,skiprows=5,skipfooter=19,engine='python')

	df.iloc[:,[4,5]]=df.iloc[:,[4,5]].applymap(myl1)
	df.iloc[:,[6]]=df.iloc[:,[6]].applymap(myl2)
	df.iloc[:,[7]]=df.iloc[:,[7]].applymap(myl3)
	df.iloc[:,[8,11]]=df.iloc[:,[8,11]].applymap(myl4)
	df.iloc[:,[9]]=df.iloc[:,[9]].applymap(myl5)
	df.iloc[:,[10]]=df.iloc[:,[10]].applymap(myl6)

	print(df)

	print('header:')
	print(headertmp)
	print('footer:')
	print(footer)

	if not os.path.exists(os.path.dirname(file.replace('avaps','windsp_avaps'))):
		try:
			os.makedirs(os.path.dirname(file.replace('avaps','windsp_avaps')))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise

	with open(file.replace('avaps','windsp_avaps'), "w") as f:
		f.write("".join(headertmp))
		f.write(df.to_csv(header=None,index=None,sep=' ').replace('"','').replace('nan','   '))
		f.write("".join(footer))

def main():
	files=glob(srcpath+"/**/*.avp", recursive=True)
	
	for file in files:
		processfile(file)

if __name__== "__main__":
	main()





