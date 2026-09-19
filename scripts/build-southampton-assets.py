"""Historical Southampton landmarks with the original ferry-terminal graphics."""
from pathlib import Path
import runpy
R=Path(__file__).resolve().parents[1]
build=runpy.run_path(str(R/'scripts/build-capital-assets.py'))['build']
build('SouthamptonPast',[('bargate',(0,0,890,1024),(96,64)),('tudor',(890,0,1536,540),(80,64)),('wall',(890,540,1536,1024),(32,64))],'southampton-source.png',mask_palette=True,base_name='island_harbor',base_tiles=165)
