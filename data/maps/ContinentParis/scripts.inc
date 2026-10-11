ContinentParis_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentParis_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentParis_Transition
 .byte 0
ContinentParis_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentParis_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
