ContinentValletta_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentValletta_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentValletta_Transition
 .byte 0
ContinentValletta_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentValletta_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
