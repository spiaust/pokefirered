"""Native windows and a side study desk for Magdalen's visitor room."""
from pathlib import Path
import struct
R=Path(__file__).resolve().parents[1]
def build():
 a=list(struct.unpack('<130H',(R/'data/layouts/EuropeBerlinLibrary/map.bin').read_bytes()))
 for x in range(1,13):
  a[x]=(a[x]&0xfc00)|0x20;a[13+x]=(a[13+x]&0xfc00)|0x28;a[26+x]=(a[26+x]&0xfc00)|0x09
 for bx in (3,9):
  for y,row in enumerate([(0x0d,0x0e),(0x15,0x16)]):
   for dx,t in enumerate(row):i=y*13+bx+dx;a[i]=(a[i]&0xfc00)|t
 for y in (4,5):
  for x in (6,7):a[y*13+x]=0x3001
 for dy,row in enumerate([(0x44c,0x44d),(0x454,0x455)]):
  for dx,t in enumerate(row):a[(5+dy)*13+8+dx]=t
 p=R/'data/layouts/EuropeMagdalenVisitor/map.bin';data=struct.pack('<130H',*a)
 if p.read_bytes()!=data:p.write_bytes(data)
if __name__=='__main__':build()
