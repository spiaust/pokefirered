ContinentLondon_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentLondon_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentLondon_Transition
 .byte 0
ContinentLondon_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentLondon_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
