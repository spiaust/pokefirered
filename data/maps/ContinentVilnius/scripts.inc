ContinentVilnius_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentVilnius_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentVilnius_Transition
 .byte 0
ContinentVilnius_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentVilnius_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
