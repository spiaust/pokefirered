@ Optional post-ending chapter. Native variables are separate from the main story.
EuropeArchive_Oxford::
 lock
 faceplayer
 goto_if_ne VAR_EUROPE_MAIN_CONCLUDED, 1, EuropeArchive_Locked
 goto_if_eq VAR_EUROPE_ARCHIVE_STORY, 2, EuropeArchive_Done
 goto_if_eq VAR_EUROPE_ARCHIVE_STORY, 1, EuropeArchive_OxfordNote
 msgbox EuropeArchive_OfferText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeArchive_End
 setvar VAR_EUROPE_ARCHIVE_STORY, 1
 setvar VAR_EUROPE_ARCHIVE_OXFORD, 0
 setvar VAR_EUROPE_ARCHIVE_CHANTILLY, 0
 setvar VAR_EUROPE_ARCHIVE_ORAN, 0
 msgbox EuropeArchive_DirectionsText
EuropeArchive_OxfordNote::
 goto_if_eq VAR_EUROPE_ARCHIVE_OXFORD, 1, EuropeArchive_Noted
 msgbox EuropeArchive_OxfordQuestion, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeArchive_Retry
 setvar VAR_EUROPE_ARCHIVE_OXFORD, 1
 msgbox EuropeArchive_OxfordText
 goto EuropeArchive_End

EuropeArchive_Chantilly::
 lock
 faceplayer
 goto_if_eq VAR_EUROPE_ARCHIVE_STORY, 2, EuropeArchive_Done
 goto_if_ne VAR_EUROPE_ARCHIVE_STORY, 1, EuropeArchive_NotStarted
 goto_if_eq VAR_EUROPE_ARCHIVE_CHANTILLY, 1, EuropeArchive_Noted
 msgbox EuropeArchive_ChantillyQuestion, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeArchive_Retry
 setvar VAR_EUROPE_ARCHIVE_CHANTILLY, 1
 msgbox EuropeArchive_ChantillyText
 goto EuropeArchive_End

EuropeArchive_Oran::
 lock
 faceplayer
 goto_if_eq VAR_EUROPE_ARCHIVE_STORY, 2, EuropeArchive_Done
 goto_if_ne VAR_EUROPE_ARCHIVE_STORY, 1, EuropeArchive_NotStarted
 goto_if_eq VAR_EUROPE_ARCHIVE_ORAN, 1, EuropeArchive_Noted
 msgbox EuropeArchive_OranQuestion, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeArchive_Retry
 setvar VAR_EUROPE_ARCHIVE_ORAN, 1
 msgbox EuropeArchive_OranText
 goto EuropeArchive_End

EuropeArchive_Report::
 goto_if_ne VAR_EUROPE_ARCHIVE_OXFORD, 1, EuropeArchive_Incomplete
 goto_if_ne VAR_EUROPE_ARCHIVE_CHANTILLY, 1, EuropeArchive_Incomplete
 goto_if_ne VAR_EUROPE_ARCHIVE_ORAN, 1, EuropeArchive_Incomplete
 checkitemspace ITEM_PP_UP, 1
 goto_if_eq VAR_RESULT, FALSE, EuropeArchive_Full
 msgbox EuropeArchive_ConclusionText
 showmonpic SPECIES_CELEBI, 10, 3
 waitbuttonpress
 hidemonpic
 giveitem ITEM_PP_UP, 1
 setvar VAR_EUROPE_ARCHIVE_STORY, 2
 goto EuropeCelebi_End
EuropeArchive_Incomplete::
 msgbox EuropeArchive_DirectionsText
 goto EuropeCelebi_MainResearcher
EuropeArchive_Full::
 msgbox EuropeArchive_FullText
 goto EuropeCelebi_End
EuropeArchive_Noted::
 msgbox EuropeArchive_NotedText
 goto EuropeArchive_End
EuropeArchive_Retry::
 msgbox EuropeArchive_RetryText
 goto EuropeArchive_End
EuropeArchive_NotStarted::
 msgbox EuropeArchive_NotStartedText
 goto EuropeArchive_End
EuropeArchive_Locked::
 msgbox EuropeArchive_LockedText
 goto EuropeArchive_End
EuropeArchive_Done::
 msgbox EuropeArchive_DoneText
EuropeArchive_End::
 release
 end

EuropeArchive_OfferText::
 .string "CELEBI: LETTERS FOR TOMORROW\n"
 .string "ADA's account inspired our archive.\p"
 .string "CELEBI worries those small acts of\n"
 .string "care will be forgotten again.\p"
 .string "Will you help three reading rooms\n"
 .string "make honest records for the future?$"
EuropeArchive_DirectionsText::
 .string "Meet the archive researchers in\n"
 .string "three modern visitor rooms:\p"
 .string "OXFORD: RADCLIFFE SQUARE (38,10).\n"
 .string "CHANTILLY: CHATEAU (51,11).\p"
 .string "ORANIENBURG: PALACE (48,9).\n"
 .string "Speak to each central researcher.\p"
 .string "Read the question and answer YES\n"
 .string "to record its lesson.\p"
 .string "Return all three notes to ADA in\n"
 .string "OXFORD. Trains connect the towns.$"
EuropeArchive_OxfordQuestion::
 .string "This letter has a date and author.\n"
 .string "Those details let us check it.\p"
 .string "Keep the date and author beside\n"
 .string "the copied words in our archive?$"
EuropeArchive_OxfordText::
 .string "OXFORD NOTE RECORDED: SOURCES.\n"
 .string "Keep a record's date and author.\p"
 .string "A caring story deserves the same\n"
 .string "honesty as any important account.$"
EuropeArchive_ChantillyQuestion::
 .string "A restored display is not the\n"
 .string "same as an untouched old object.\p"
 .string "Label what is original and what\n"
 .string "was restored in our new record?$"
EuropeArchive_ChantillyText::
 .string "CHANTILLY NOTE RECORDED: CONTEXT.\n"
 .string "Label restoration and uncertainty.\p"
 .string "We can admire a place while being\n"
 .string "clear about what survives today.$"
EuropeArchive_OranQuestion::
 .string "A witness shared a personal story.\n"
 .string "They should choose how it is used.\p"
 .string "Ask their permission before adding\n"
 .string "their name to our public archive?$"
EuropeArchive_OranText::
 .string "ORANIENBURG NOTE RECORDED: CARE.\n"
 .string "Respect each witness's choices.\p"
 .string "The people in our records are more\n"
 .string "than a name beside a date.$"
EuropeArchive_ConclusionText::
 .string "ADA: Three notes, one living archive.\n"
 .string "Sources, context and care.\p"
 .string "CELEBI's journey belongs to those\n"
 .string "who offered shelter and honest news.\p"
 .string "Your new records keep their work\n"
 .string "visible without changing their past.\p"
 .string "CELEBI knows these letters will\n"
 .string "have readers tomorrow. Thank you!\p"
 .string "LETTERS FOR TOMORROW COMPLETE!\n"
 .string "Take this PP UP for your partner.$"
EuropeArchive_NotedText::
 .string "Your note from this room is saved.\n"
 .string "Bring all three notes to ADA.$"
EuropeArchive_RetryText::
 .string "No note was recorded. Read the\n"
 .string "question again whenever you like.$"
EuropeArchive_NotStartedText::
 .string "Our archive project starts in the\n"
 .string "RADCLIFFE visitor room in OXFORD.\p"
 .string "Speak to its central researcher\n"
 .string "after ADA's main-story conclusion.$"
EuropeArchive_LockedText::
 .string "Finish CELEBI's journey with ADA\n"
 .string "before starting our archive project.$"
EuropeArchive_DoneText::
 .string "LETTERS FOR TOMORROW is complete.\n"
 .string "Your three notes remain here.\p"
 .string "Thank you for helping CELEBI keep\n"
 .string "these stories safe for tomorrow.$"
EuropeArchive_FullText::
 .string "Your three notes are safe. Make\n"
 .string "room for one PP UP in BAG, ITEMS.\p"
 .string "Then return to ADA to finish\n"
 .string "LETTERS FOR TOMORROW.$"
