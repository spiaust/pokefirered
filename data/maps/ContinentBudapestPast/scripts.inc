ContinentBudapestPast_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentBudapestPast_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentBudapestPast_Transition
 .byte 0
ContinentBudapestPast_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentBudapestPast_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
