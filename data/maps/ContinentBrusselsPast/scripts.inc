ContinentBrusselsPast_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentBrusselsPast_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentBrusselsPast_Transition
 .byte 0
ContinentBrusselsPast_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentBrusselsPast_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
