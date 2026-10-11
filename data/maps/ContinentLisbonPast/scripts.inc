ContinentLisbonPast_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentLisbonPast_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentLisbonPast_Transition
 .byte 0
ContinentLisbonPast_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentLisbonPast_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
