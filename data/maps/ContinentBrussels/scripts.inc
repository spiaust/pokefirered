ContinentBrussels_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentBrussels_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentBrussels_Transition
 .byte 0
ContinentBrussels_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentBrussels_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
