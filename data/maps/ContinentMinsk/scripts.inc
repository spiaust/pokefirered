ContinentMinsk_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentMinsk_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentMinsk_Transition
 .byte 0
ContinentMinsk_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentMinsk_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
