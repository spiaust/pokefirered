ContinentIstanbulPast_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentIstanbulPast_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentIstanbulPast_Transition
 .byte 0
ContinentIstanbulPast_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentIstanbulPast_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
