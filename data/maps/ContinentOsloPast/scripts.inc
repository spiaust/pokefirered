ContinentOsloPast_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentOsloPast_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentOsloPast_Transition
 .byte 0
ContinentOsloPast_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentOsloPast_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
