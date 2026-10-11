ContinentLuxembourg_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentLuxembourg_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentLuxembourg_Transition
 .byte 0
ContinentLuxembourg_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentLuxembourg_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
