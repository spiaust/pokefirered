ContinentZagreb_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentZagreb_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentZagreb_Transition
 .byte 0
ContinentZagreb_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentZagreb_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
