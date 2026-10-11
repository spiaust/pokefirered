ContinentKyiv_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentKyiv_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentKyiv_Transition
 .byte 0
ContinentKyiv_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentKyiv_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
