ContinentRome_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentRome_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentRome_Transition
 .byte 0
ContinentRome_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentRome_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
