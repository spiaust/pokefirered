ContinentLjubljana_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentLjubljana_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentLjubljana_Transition
 .byte 0
ContinentLjubljana_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentLjubljana_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
