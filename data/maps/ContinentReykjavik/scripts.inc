ContinentReykjavik_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentReykjavik_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentReykjavik_Transition
 .byte 0
ContinentReykjavik_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentReykjavik_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
