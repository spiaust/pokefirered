ContinentWarsaw_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentWarsaw_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentWarsaw_Transition
 .byte 0
ContinentWarsaw_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentWarsaw_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
