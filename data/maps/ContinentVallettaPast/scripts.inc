ContinentVallettaPast_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentVallettaPast_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentVallettaPast_Transition
 .byte 0
ContinentVallettaPast_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentVallettaPast_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
