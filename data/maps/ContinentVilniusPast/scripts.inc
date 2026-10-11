ContinentVilniusPast_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentVilniusPast_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentVilniusPast_Transition
 .byte 0
ContinentVilniusPast_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentVilniusPast_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
