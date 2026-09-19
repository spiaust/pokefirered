EuropeSupplies_Clerk::
	goto_if_questlog EventScript_ReleaseEnd
	lock
	faceplayer
	message EuropeSupplies_Text_Welcome
	waitmessage
	pokemart EuropeSupplies_Items
	msgbox EuropeSupplies_Text_Goodbye
	release
	end

	.align 2
EuropeSupplies_Items::
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_REPEL
	.2byte ITEM_NONE

EuropeSupplies_Text_Welcome::
	.string "Traveling supplies!\n"
	.string "How may I help you?$"

EuropeSupplies_Text_Goodbye::
	.string "Have a good trip!\n"
	.string "Clinics heal your team for free.$"
