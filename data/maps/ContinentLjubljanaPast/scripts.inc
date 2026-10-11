ContinentLjubljanaPast_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentLjubljanaPast_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentLjubljanaPast_Transition
 .byte 0
ContinentLjubljanaPast_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentLjubljanaPast_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
