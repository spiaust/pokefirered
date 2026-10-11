ContinentBerlinPast_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentBerlinPast_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentBerlinPast_Transition
 .byte 0
ContinentBerlinPast_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentBerlinPast_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
