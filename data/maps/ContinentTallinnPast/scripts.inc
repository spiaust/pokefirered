ContinentTallinnPast_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentTallinnPast_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentTallinnPast_Transition
 .byte 0
ContinentTallinnPast_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentTallinnPast_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
