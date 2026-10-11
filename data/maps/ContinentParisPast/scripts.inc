ContinentParisPast_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentParisPast_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentParisPast_Transition
 .byte 0
ContinentParisPast_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentParisPast_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
