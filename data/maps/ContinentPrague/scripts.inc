ContinentPrague_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentPrague_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentPrague_Transition
 .byte 0
ContinentPrague_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentPrague_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
