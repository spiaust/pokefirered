ContinentRiga_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentRiga_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentRiga_Transition
 .byte 0
ContinentRiga_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentRiga_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
