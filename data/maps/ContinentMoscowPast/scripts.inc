ContinentMoscowPast_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentMoscowPast_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentMoscowPast_Transition
 .byte 0
ContinentMoscowPast_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentMoscowPast_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
