ContinentSkopje_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentSkopje_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentSkopje_Transition
 .byte 0
ContinentSkopje_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentSkopje_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
