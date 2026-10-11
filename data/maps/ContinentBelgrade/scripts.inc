ContinentBelgrade_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentBelgrade_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentBelgrade_Transition
 .byte 0
ContinentBelgrade_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentBelgrade_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
