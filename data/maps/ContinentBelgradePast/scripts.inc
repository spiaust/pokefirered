ContinentBelgradePast_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentBelgradePast_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentBelgradePast_Transition
 .byte 0
ContinentBelgradePast_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentBelgradePast_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
