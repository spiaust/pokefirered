ContinentTirana_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentTirana_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentTirana_Transition
 .byte 0
ContinentTirana_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentTirana_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
