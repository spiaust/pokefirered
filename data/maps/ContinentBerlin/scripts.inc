ContinentBerlin_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentBerlin_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentBerlin_Transition
 .byte 0
ContinentBerlin_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentBerlin_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
