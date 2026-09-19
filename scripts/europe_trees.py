"""Arrange complete native trees without changing map collision footprints."""
TREE={0xe,0xf,*range(0x14,0x18),*range(0x1c,0x20),*range(0x24,0x28)}
def finish_trees(a):
 h=len(a);w=len(a[0]);mask={(x,y) for y,row in enumerate(a) for x,t in enumerate(row) if t&0xc00 and t&1023 in TREE};done=set()
 for x in range(0,w-1,2):
  y=0
  while y<h:
   if (x,y) not in mask or (x+1,y) not in mask:y+=1;continue
   start=y
   while y<h and (x,y) in mask and (x+1,y) in mask:y+=1
   end=y;row=start
   while row<end:
    n=min(4,end-row)
    # Four rows form one complete tree. Short edges use a compact crown
    # or low shrubs instead of half trees or repeated trunk/canopy rows.
    pattern={4:[0xe,0x14,0x1c,0x24],3:[0xe,0x1c,0x24],2:[0x12,0x23],1:[5]}[n]
    for dy,t in enumerate(pattern):
     for dx in (0,1):
      xx,yy=x+dx,row+dy;a[yy][xx]=(a[yy][xx]&~1023)|(t+dx if n>2 else t);done.add((xx,yy))
    row+=n
 for x,y in mask-done:a[y][x]=(a[y][x]&~1023)|5
 return a
