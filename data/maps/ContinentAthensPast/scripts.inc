ContinentAthensPast_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentAthensPast_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentAthensPast_Transition
 .byte 0
ContinentAthensPast_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentAthensPast_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
