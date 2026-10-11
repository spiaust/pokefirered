ContinentIstanbul_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentIstanbul_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentIstanbul_Transition
 .byte 0
ContinentIstanbul_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentIstanbul_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
