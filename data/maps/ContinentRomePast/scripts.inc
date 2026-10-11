ContinentRomePast_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentRomePast_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentRomePast_Transition
 .byte 0
ContinentRomePast_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentRomePast_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
