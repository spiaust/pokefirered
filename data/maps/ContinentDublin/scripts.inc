ContinentDublin_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentDublin_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentDublin_Transition
 .byte 0
ContinentDublin_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentDublin_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
