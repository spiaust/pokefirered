ContinentKyivPast_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentKyivPast_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentKyivPast_Transition
 .byte 0
ContinentKyivPast_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentKyivPast_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
