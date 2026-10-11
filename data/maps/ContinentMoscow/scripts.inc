ContinentMoscow_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentMoscow_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentMoscow_Transition
 .byte 0
ContinentMoscow_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentMoscow_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
