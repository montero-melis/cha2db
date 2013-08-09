.echo on
.mode column
.headers on
.nullvalue NULL


-- Problem: some words in the database end with a comma ',' or any other pattern which shows you that sth's wrong
-- Goal: try to see where these words come from (when are they populated into the db) to work on a solution
-- How many words in the database do end with a comma (but substitute with other unwanted pattern as well)?
SELECT COUNT(*) FROM Words WHERE word LIKE '%,';
-- Query: 
SELECT w.id, w.word, p.name, dm.role, v.videoname
FROM DescrMatrix dm
	INNER JOIN Words w ON dm.word_id=w.id
	INNER JOIN Videos v ON dm.video_id=v.id
	INNER JOIN Interaction i ON dm.interaction_id=i.id
	INNER JOIN Participant p ON i.participant_id=p.id
WHERE w.word LIKE '%,'
;


-- How many participants per language
SELECT groupname, COUNT(*) FROM Participant GROUP BY groupname;


-- WORDS
-- 

-- How many unique words are there in the db per language?
SELECT language, COUNT(Words.word)
FROM Words
GROUP BY language;
-- Same, but consider only target items and participant descriptions
-- ATTENTION, NEEDS CHANGES AFTER CHANGING DB SCHEMA!!!
SELECT Words.language, COUNT(DISTINCT lt.word_id)
FROM LingTask lt
	INNER JOIN Videos v ON lt.video_id=v.id
	INNER JOIN Participant p ON lt.participant_id=p.id
	INNER JOIN Words w ON w.id=lt.word_id
WHERE v.videotype IN ('target') AND dm.role='*SUJ'
GROUP BY .language_id
;

-- Type/token ratio per language (divide both measures -- couldn't figure out how to get the ratio directly)
-- for Swedish target descriptions only
SELECT l.language, 
	COUNT(DISTINCT word_id) AS nbTypes,
	(SELECT COUNT(*)
		FROM DescrMatrix dm
			INNER JOIN Videos v ON dm.video_id=v.id
			INNER JOIN Interaction i ON dm.interaction_id=i.id
			INNER JOIN Language l ON i.language_id=l.id
		WHERE v.videotype IN ('target') AND dm.role='*SUJ' AND l.language="swe") AS nbTokens
FROM DescrMatrix dm
	INNER JOIN Videos v ON dm.video_id=v.id
	INNER JOIN Interaction i ON dm.interaction_id=i.id
	INNER JOIN Language l ON i.language_id=l.id
WHERE v.videotype IN ('target') AND dm.role='*SUJ' AND l.language="swe"
;
-- for Spanish target descriptions only
SELECT l.language, 
	COUNT(DISTINCT word_id) AS nbTypes,
	(SELECT COUNT(*)
		FROM DescrMatrix dm
			INNER JOIN Videos v ON dm.video_id=v.id
			INNER JOIN Interaction i ON dm.interaction_id=i.id
			INNER JOIN Language l ON i.language_id=l.id
		WHERE v.videotype IN ('target') AND dm.role='*SUJ' AND l.language="spa") AS nbTokens
FROM DescrMatrix dm
	INNER JOIN Videos v ON dm.video_id=v.id
	INNER JOIN Interaction i ON dm.interaction_id=i.id
	INNER JOIN Language l ON i.language_id=l.id
WHERE v.videotype IN ('target') AND dm.role='*SUJ' AND l.language="spa"
;


-- What are the n most frequent words independently of language?
SELECT w.word, w.language_id, COUNT(dm.word_id) AS nbOccurrences
FROM DescrMatrix dm 
	INNER JOIN Words w ON dm.word_id=w.id
GROUP BY dm.word_id
ORDER BY nbOccurrences DESC
LIMIT 20
;

-- What are the n most frequent words in each language? 
-- NB: prints 2 lists
SELECT w.word, w.language_id, COUNT(dm.word_id) AS nbOccurrences
FROM DescrMatrix dm INNER JOIN Words w ON dm.word_id=w.id
WHERE w.language_id=1
GROUP BY dm.word_id
ORDER BY nbOccurrences DESC
LIMIT 20
;
SELECT w.word, w.language_id, COUNT(dm.word_id) AS nbOccurrences
FROM DescrMatrix dm INNER JOIN Words w ON dm.word_id=w.id
WHERE w.language_id=2
GROUP BY dm.word_id
ORDER BY nbOccurrences DESC
LIMIT 20
;
-- same (also two separate lists) but for participant descriptions of target items only
-- Spanish
SELECT w.word, w.language_id, COUNT(dm.word_id) AS nbOccurrences
FROM DescrMatrix dm 
	INNER JOIN Words w ON dm.word_id=w.id
	INNER JOIN Videos v ON dm.video_id=v.id
	INNER JOIN Interaction i ON dm.interaction_id=i.id
	INNER JOIN Language l ON i.language_id=l.id
WHERE w.language_id=1 AND v.videotype IN ('target') AND dm.role='*SUJ'
GROUP BY dm.word_id
ORDER BY nbOccurrences DESC
LIMIT 20
;
-- Swedish
SELECT w.word, w.language_id, COUNT(dm.word_id) AS nbOccurrences
FROM DescrMatrix dm 
	INNER JOIN Words w ON dm.word_id=w.id
	INNER JOIN Videos v ON dm.video_id=v.id
	INNER JOIN Interaction i ON dm.interaction_id=i.id
	INNER JOIN Language l ON i.language_id=l.id
WHERE w.language_id=2 AND v.videotype IN ('target') AND dm.role='*SUJ'
GROUP BY dm.word_id
ORDER BY nbOccurrences DESC
LIMIT 20
;




-- Word length
-- 20 longest words in db
SELECT word, LENGTH(word) AS length FROM Words ORDER BY length DESC LIMIT 20;
-- Longest word for each language:
--  Spanish
SELECT word, LENGTH(word) AS length FROM Words 
WHERE language_id = 1
ORDER BY length DESC LIMIT 5;
-- Swedish
SELECT word, LENGTH(word) AS length FROM Words 
WHERE language_id = 2
ORDER BY length DESC LIMIT 5;
-- Average length for each language


-- USEFUL
-- 

-- Data from which to create documents using 'createDocs.py'
SELECT p.name, v.videoname, w.word, l.language
FROM DescrMatrix dm
    INNER JOIN Words w ON dm.word_id=w.id
    INNER JOIN Videos v ON dm.video_id=v.id
    INNER JOIN Interaction i ON dm.interaction_id=i.id
    INNER JOIN Participant p ON i.participant_id=p.id
    INNER JOIN Language l ON i.language_id=l.id
WHERE dm.role='*SUJ' AND v.videoname NOT IN ('prt_meuche','closing')
;


-- Average description length (target items only)
-- NB: multiply by 1.0 in order to convert integer division to floating point division
-- all participants
SELECT AVG(countpervideo)
FROM
	(SELECT COUNT(*)*1.0/(SELECT COUNT(*) FROM Participant) AS countpervideo
	FROM DescrMatrix dm
		INNER JOIN videos v ON dm.video_id=v.id
	WHERE dm.role='*SUJ' AND v.videotype='target'
	GROUP BY dm.video_id)
;
-- Swedish only
SELECT AVG(countpervideo)
FROM
	(SELECT COUNT(*)*1.0/(SELECT COUNT(*) FROM Participant WHERE partGroup_id=2) AS countpervideo
	FROM DescrMatrix dm
		INNER JOIN videos v ON dm.video_id=v.id
		INNER JOIN Interaction i ON dm.interaction_id=i.id
	WHERE dm.role='*SUJ' AND v.videotype='target' AND i.language_id=2
	GROUP BY dm.video_id)
;
-- Spanish only
SELECT AVG(countpervideo)
FROM
	(SELECT COUNT(*)*1.0/(SELECT COUNT(*) FROM Participant WHERE partGroup_id=1) AS countpervideo
	FROM DescrMatrix dm
		INNER JOIN videos v ON dm.video_id=v.id
		INNER JOIN Interaction i ON dm.interaction_id=i.id
	WHERE dm.role='*SUJ' AND v.videotype='target' AND i.language_id=1
	GROUP BY dm.video_id)
;


-- Average description length per item (target items only)
-- all participants
SELECT v.videoname, COUNT(*)*1.0/(SELECT COUNT(*) FROM Participant) AS wordspervideo
FROM DescrMatrix dm
	INNER JOIN videos v ON dm.video_id=v.id
WHERE dm.role='*SUJ' AND v.videotype='target'
GROUP BY dm.video_id
;
-- Swedish only
SELECT v.videoname, COUNT(*)*1.0/(SELECT COUNT(*) FROM Participant WHERE partGroup_id=2) AS wordspervideo
FROM DescrMatrix dm
	INNER JOIN videos v ON dm.video_id=v.id
	INNER JOIN Interaction i ON dm.interaction_id=i.id
WHERE dm.role='*SUJ' AND v.videotype='target' AND i.language_id=2
GROUP BY dm.video_id
;
-- Spanish only
SELECT v.videoname, COUNT(*)*1.0/(SELECT COUNT(*) FROM Participant WHERE partGroup_id=1) AS wordspervideo
FROM DescrMatrix dm
	INNER JOIN videos v ON dm.video_id=v.id
	INNER JOIN Interaction i ON dm.interaction_id=i.id
WHERE dm.role='*SUJ' AND v.videotype='target' AND i.language_id=1
GROUP BY dm.video_id
;



-- List of all words actually used, repeating each word as often as it has been used
-- this can be used as input for some R functions like 'zipf.fnc' (package 'languageR')
-- Swedish
SELECT w.word
FROM DescrMatrix dm
	INNER JOIN Words w ON dm.word_id=w.id
	INNER JOIN Videos v ON dm.video_id=v.id
	INNER JOIN Interaction i ON dm.interaction_id=i.id
	INNER JOIN Language l ON i.language_id=l.id
WHERE v.videotype IN ('target') AND dm.role='*SUJ' AND l.language="swe"
;
-- Spanish
SELECT w.word
FROM DescrMatrix dm
	INNER JOIN Words w ON dm.word_id=w.id
	INNER JOIN Videos v ON dm.video_id=v.id
	INNER JOIN Interaction i ON dm.interaction_id=i.id
	INNER JOIN Language l ON i.language_id=l.id
WHERE v.videotype IN ('target') AND dm.role='*SUJ' AND l.language="spa"
;


-- In order to save SQL output to csv format and put back output to standard
.echo off
.headers on
.nullvalue NULL
.mode csv
.output filename.csv
SELECT column FROM table;
.output stdout
