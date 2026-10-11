from pathlib import Path
import struct
r=Path.cwd();rom=(r/'pokefirered.gba').read_bytes();symbols={}
for line in (r/'pokefirered.sym').read_text().splitlines():
 p=line.split()
 if len(p)>=4:
  try:symbols[p[-1]]=int(p[0],16)
  except ValueError:pass
for name in ('EuropeLondon','EuropeLondonReadingRoom','EuropeCouncilHall'):
 a=symbols[name+'_Layout']-0x08000000;w,h,border,cells=struct.unpack_from('<4I',rom,a)
 source=(r/'data/layouts'/name/'map.bin').read_bytes();assert rom[cells-0x08000000:cells-0x08000000+w*h*2]==source,name
 print('PASS: '+name+' source terrain matches the tested ROM byte-for-byte')
