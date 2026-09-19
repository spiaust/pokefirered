"""Compile historical Le Havre landmarks, preserving the original harbor tiles."""
from pathlib import Path
from PIL import Image
import runpy
R=Path(__file__).resolve().parents[1]
build=runpy.run_path(str(R/'scripts/build-capital-assets.py'))['build']
source='le-havre-source.png';w,h=Image.open(R/'graphics/europe/landmarks'/source).size
build('LeHavrePast',[('church',(0,0,1050,h),(96,64)),('house',(1050,0,w,h),(64,80))],source,mask_palette=True,base_name='island_harbor',base_tiles=165)
