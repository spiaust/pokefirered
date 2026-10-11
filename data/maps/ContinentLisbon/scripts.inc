ContinentLisbon_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentLisbon_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentLisbon_Transition
 .byte 0
ContinentLisbon_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentLisbon_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
