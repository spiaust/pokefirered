ContinentViennaPast_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentViennaPast_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentViennaPast_Transition
 .byte 0
ContinentViennaPast_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentViennaPast_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
