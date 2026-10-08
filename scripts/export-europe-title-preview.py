"""Export the actual emulator capture as a scaled animated preview."""
from pathlib import Path
from PIL import Image
import json
r=Path(__file__).resolve().parents[1]
paths=json.loads((r/'test-output/europe-title-frames.json').read_text())
images=[]
for name in paths:
 with Image.open(r/'test-output'/name) as im:
  images.append(im.convert('RGB').resize((720,480),Image.Resampling.NEAREST))
images[0].save(r/'test-output/europe-title.gif',save_all=True,append_images=images[1:],duration=268,loop=0)
for im in images:im.close()
print('Exported native splash animation preview')
