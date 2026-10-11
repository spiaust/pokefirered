ContinentKotor_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentKotor_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentKotor_Transition
 .byte 0
ContinentKotor_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentKotor_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
