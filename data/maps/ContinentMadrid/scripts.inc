ContinentMadrid_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentMadrid_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentMadrid_Transition
 .byte 0
ContinentMadrid_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentMadrid_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
