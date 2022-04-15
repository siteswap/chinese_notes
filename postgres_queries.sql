
select current_user, session_user;
\du
\dt


SELECT revs.ease, revs.time_seconds, revs.phrase_segmented, words.word 
FROM 
	public.catalogue_reviews revs
JOIN 	public.catalogue_knownword words
	ON revs.word_id = words.id


UPDATE public.catalogue_phrase p
SET card_type = 'PRODUCTION'
FROM public.catalogue_deck d
WHERE p.deck_id = d.id AND d.translation_only


SELECT 
	p.phrase, p.deck_id, d.id, p.include_hanzi, d.include_hanzi, p.translation_only, d.translation_only
FROM 
	public.catalogue_phrase p
INNER JOIN public.catalogue_deckword dw
	ON dw.word_id = p.id
INNER JOIN public.catalogue_deck d
	ON dw.deck_id = d.id
ORDER BY p.id ASC LIMIT 100

