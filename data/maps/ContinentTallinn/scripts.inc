ContinentTallinn_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentTallinn_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentTallinn_Transition
 .byte 0
ContinentTallinn_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentTallinn_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
