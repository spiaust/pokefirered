ContinentPraguePast_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentPraguePast_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentPraguePast_Transition
 .byte 0
ContinentPraguePast_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentPraguePast_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
