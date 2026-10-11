ContinentBucharestPast_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentBucharestPast_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentBucharestPast_Transition
 .byte 0
ContinentBucharestPast_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentBucharestPast_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
