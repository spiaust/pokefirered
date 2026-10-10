"""Compile Oxford/Chantilly/Oranienburg artwork with the shared GBA pipeline."""
from pathlib import Path
from PIL import Image
import runpy,sys
R=Path(__file__).resolve().parents[1]
build=runpy.run_path(str(R/'scripts/build-capital-assets.py'))['build']
for city in sys.argv[1:] or ['Oxford','Chantilly','Oranienburg']:
 source=city.lower()+'-source.png';w,h=Image.open(R/'graphics/europe/landmarks'/source).size
 specs={
  'Oxford':[('camera',(0,0,w//2,h),(64,64)),('magdalen',(w//2,0,w,h),(48,80))],
  'Chantilly':[('chateau',(0,0,w//2,h),(96,80)),('stables',(w//2,0,w,h),(96,48))],
  'Oranienburg':[('palace',(0,0,w,h),(128,64))],
 }[city]
 build(city,specs,source,mask_palette=True)
 if city=='Oxford':
  from oxford_bridges import build as build_bridges
  build_bridges()
  from oxford_gym_roof import build as build_gym_roof
  build_gym_roof()
  from oxford_station_roof import build as build_station_roof
  build_station_roof()
  from oxford_clinic_wall import build as build_clinic_wall
  build_clinic_wall()
 if city=='Chantilly':
  from chantilly_bridge import build as build_bridge
  build_bridge()
  from chantilly_gym_roof import build as build_water_roof
  build_water_roof()
  from chantilly_station_roof import build as build_french_station
  build_french_station()
  from chantilly_clinic_wall import build as build_french_clinic
  build_french_clinic()
 if city=='Oranienburg':
  from oranienburg_bridges import build as build_havel
  build_havel()
  from oranienburg_gym_roof import build as build_electric_roof
  build_electric_roof()
  from oranienburg_station_roof import build as build_german_station
  build_german_station()
  from oranienburg_clinic_wall import build as build_german_clinic
  build_german_clinic()
 from regional_clinic_sign import build as build_clinic_sign
 build_clinic_sign(city)

 from regional_station_sign import build as build_station_sign
 build_station_sign(city)
 from regional_gym_sign import build as build_gym_sign
 build_gym_sign(city)
 if city=='Oxford':
  from oxford_station_wall import build as build_station_wall
  build_station_wall()
 if city=='Chantilly':
  from chantilly_station_wall import build as build_station_wall
  build_station_wall()
 if city=='Oranienburg':
  from oranienburg_station_wall import build as build_station_wall
  build_station_wall()
