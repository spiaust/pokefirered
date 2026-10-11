ContinentSarajevo_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentSarajevo_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentSarajevo_Transition
 .byte 0
ContinentSarajevo_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentSarajevo_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
