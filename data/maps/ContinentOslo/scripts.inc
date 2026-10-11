ContinentOslo_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentOslo_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentOslo_Transition
 .byte 0
ContinentOslo_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentOslo_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
