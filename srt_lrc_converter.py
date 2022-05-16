

import re
from sys import argv

pattern=r'(?P<id>\d+)\r?\n(?P<start_time>(?P<normal>\d+:\d+:)(?P<before>\d+),(?P<after>\d+)) --> (?P<end_time>\d+:\d+:\d+,\d+)\r?\n(?P<words>.*)'


srtfile=open(argv[1],'r')

srtstr=''
for line in srtfile.readlines():
    srtstr=srtstr+line

srtfile.close()

elements=re.findall(pattern,srtstr)

lcrstr=''
for i in elements:
    lcrstr=lcrstr+'['+'%.2d'%(60*int(i[2][0:2])+int(i[2][3:5]))+':'+i[3]+'.'+i[4][0:2]+']'+i[6]+'\n'

outpath=argv[1].replace('srt','lrc')
lcrfile=open(outpath,'w')
lcrfile.write(lcrstr)
lcrfile.close()