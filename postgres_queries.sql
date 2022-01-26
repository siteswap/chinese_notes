SELECT revs.ease, revs.time_seconds, revs.phrase_segmented, words.word FROM public.catalogue_reviews revs
join public.catalogue_knownword words
on revs.word_id = words.id

