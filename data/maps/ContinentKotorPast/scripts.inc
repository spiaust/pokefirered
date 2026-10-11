ContinentKotorPast_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentKotorPast_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentKotorPast_Transition
 .byte 0
ContinentKotorPast_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentKotorPast_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
