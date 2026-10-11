"""Build six original 32x32 rental mount frames in the native player palette.
The blue body, pale shell, horn and flippers avoid the skin-color slots.
This is a code-authored sprite asset, not a modified source Pokemon image.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def frame(direction,phase):
 p=[[0]*32 for _ in range(32)]
 def ellipse(x0,y0,x1,y1,c):
  cx=(x0+x1)/2;cy=(y0+y1)/2;rx=(x1-x0+1)/2;ry=(y1-y0+1)/2
  for y in range(max(0,y0),min(32,y1+1)):
   for x in range(max(0,x0),min(32,x1+1)):
    if ((x-cx)/rx)**2+((y-cy)/ry)**2<=1:p[y][x]=c
 def dot(x,y,c):
  if 0<=x<32 and 0<=y<32:p[y][x]=c
 # Flippers and a broad blue body beneath the rider.
 ellipse(1,21+phase,11,27+phase,15);ellipse(2,22+phase,10,26+phase,5)
 ellipse(21,21-phase,30,27-phase,15);ellipse(22,22-phase,29,26-phase,7)
 ellipse(4,13,28,28,15);ellipse(5,14,27,27,6);ellipse(6,14,26,25,5)
 # Pale shell with raised plates, visible beside the player.
 ellipse(8,12,24,23,15);ellipse(9,13,23,22,10);ellipse(10,13,22,20,9)
 for x,y in ((10,15),(16,13),(22,15),(12,20),(20,20)):
  dot(x,y,10);dot(x,y-1,9)
 if direction=='south':
  ellipse(12,21,20,30,15);ellipse(13,21,19,29,5)
  ellipse(11,25,21,31,15);ellipse(12,25,20,30,7)
  dot(13,27,15);dot(19,27,15);dot(16,29,6)
  dot(16,23,9);dot(16,24,9)
 elif direction=='north':
  ellipse(12,4,20,16,15);ellipse(13,5,19,16,5)
  ellipse(11,2,21,10,15);ellipse(12,3,20,9,7)
  dot(15,1,9);dot(15,2,9);dot(16,3,9)
 else:
  ellipse(6,9,13,25,15);ellipse(7,10,12,24,5)
  ellipse(1,8,13,16,15);ellipse(2,9,12,15,7)
  dot(4,11,15);dot(2,13,6);dot(6,7,9);dot(6,6,9);dot(7,8,9)
 return p

def encode(p):
 out=bytearray()
 for ty in range(4):
  for tx in range(4):
   for y in range(8):
    for x in range(0,8,2):out.append(p[ty*8+y][tx*8+x]|(p[ty*8+y][tx*8+x+1]<<4))
 return out

def build():
 result=b''.join(encode(frame(d,p)) for d in ('south','north','west') for p in (0,1))
 assert len(result)==3072
 target=ROOT/'graphics/object_events/pics/misc/europe_lapras_mount.4bpp'
 if not target.exists() or target.read_bytes()!=result:target.write_bytes(result)
 return result
if __name__=='__main__':build();print('Built six directional Lapras mount frames.')
