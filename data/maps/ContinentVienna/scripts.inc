ContinentVienna_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentVienna_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentVienna_Transition
 .byte 0
ContinentVienna_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentVienna_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
