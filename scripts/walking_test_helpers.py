"""Permit only native walking friendship gains; reject other party or progress changes."""
import struct,re
from emulator import ROOT

def assert_walk_preserved(before,after):
 # Walking can award friendship after 128 steps. Verify that this is the
 # only permitted party change, rather than ignoring the party snapshot.
 assert before[1:]==after[1:]
 count,old=before[0];new_count,new=after[0];assert count==new_count
 slots={int(n):int(slot) for n,slot in re.findall(r'SUBSTRUCT_CASE\(\s*(\d+),\s*(\d+),',(ROOT/'src/pokemon.c').read_text())}
 for i in range(count):
  a=bytearray(old[i*100:(i+1)*100]);b=bytearray(new[i*100:(i+1)*100])
  personality,trainer=struct.unpack_from('<II',a)
  offset=32+slots[personality%24]*12+9;key=((personality^trainer)>>8)&255
  first,last=a[offset]^key,b[offset]^key
  assert 0<=last-first<=5,('unexpected friendship change',first,last)
  if last!=first:print(f'Walking friendship: {first} -> {last}',flush=True)
  for j in (28,29,offset):a[j]=b[j]=0
  assert a==b,'walking changed other party data'

