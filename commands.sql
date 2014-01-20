.echo on
.mode column
.headers on
.nullvalue NULL

-- How many participants per language
SELECT groupname, COUNT(*) FROM Participant GROUP BY groupname;


-- How many participants per languag by counting participants in the LingTask table?
-- Should match with number in Participant table!
SELECT COUNT(DISTINCT p.name)
FROM LingTask lt
	INNER JOIN Participant p ON lt.participant_id=p.id
WHERE p.groupname='SwAD'
;


-- List of (Swedish) participants in LingTask
SELECT DISTINCT p.name
FROM LingTask lt
	INNER JOIN Participant p ON lt.participant_id=p.id
WHERE p.groupname='SwAD'
ORDER BY p.name
;



-- SQL for data export to R (will serve as input for tm package)
-- participant descriptions of target items only
SELECT p.id, p.name, p.groupname, v.videoname, v.videotype, w.language, w.word
FROM Participant p 
	INNER JOIN LingTask lt ON lt.participant_id=p.id 
	INNER JOIN Videos v ON lt.video_id=v.id
	INNER JOIN Words w ON w.id=lt.word_id
WHERE lt.role='*SUJ' AND v.videotype IN ('target')
;


-- WORDS

-- How many unique words are there in the db per language?
SELECT language, COUNT(Words.word)
FROM Words
GROUP BY language;
-- Same, but consider only target items and participant descriptions
SELECT w.language, COUNT(DISTINCT lt.word_id)
FROM LingTask lt
	INNER JOIN Videos v ON lt.video_id=v.id
	INNER JOIN Words w ON w.id=lt.word_id
WHERE v.videotype IN ('target') AND lt.role='*SUJ'
GROUP BY w.language
;


-- What are the n most frequent words independently of language?
SELECT w.word, w.language, COUNT(lt.word_id) AS nbOccurrences
FROM LingTask lt
	INNER JOIN Words w ON lt.word_id=w.id
GROUP BY lt.word_id
ORDER BY nbOccurrences DESC
LIMIT 20
;

-- What are the n most frequent words in each language? 

-- NB: prints 2 lists
SELECT w.word, w.language, COUNT(lt.word_id) AS nbOccurrences
FROM LingTask lt INNER JOIN Words w ON lt.word_id=w.id
WHERE w.language="spa"
GROUP BY lt.word_id
ORDER BY nbOccurrences DESC
LIMIT 20
;
SELECT w.word, w.language, COUNT(lt.word_id) AS nbOccurrences
FROM LingTask lt INNER JOIN Words w ON lt.word_id=w.id
WHERE w.language="swe"
GROUP BY lt.word_id
ORDER BY nbOccurrences DESC
LIMIT 20
;
-- same (also two separate lists) but for participant descriptions of target items only
-- Spanish
SELECT w.word, w.language, COUNT(lt.word_id) AS nbOccurrences
FROM LingTask lt 
	INNER JOIN Words w ON lt.word_id=w.id
	INNER JOIN Videos v ON lt.video_id=v.id
WHERE w.language="spa" AND v.videotype IN ('target') AND lt.role='*SUJ'
GROUP BY lt.word_id
ORDER BY nbOccurrences DESC
LIMIT 20
;
-- Swedish
SELECT w.word, w.language, COUNT(lt.word_id) AS nbOccurrences
FROM LingTask lt 
	INNER JOIN Words w ON lt.word_id=w.id
	INNER JOIN Videos v ON lt.video_id=v.id
WHERE w.language="swe" AND v.videotype IN ('target') AND lt.role='*SUJ'
GROUP BY lt.word_id
ORDER BY nbOccurrences DESC
LIMIT 20
;

-- One list per language of all words in alphabetic order, together with how often they occurr
-- Use this to tag the words for semantic category and PartOfSpeech
-- NB: Only words appearing in target item descriptions and uttered by subjects
-- Spanish
SELECT w.language, w.id, COUNT(lt.word_id) AS nbOccurrences, w.word
FROM LingTask lt
	INNER JOIN Words w ON lt.word_id=w.id
	INNER JOIN Videos v ON lt.video_id=v.id
WHERE w.language="spa" AND v.videotype IN ('target') AND lt.role='*SUJ'
GROUP BY lt.word_id
ORDER BY w.word 
;
-- Swedish
SELECT w.language, w.id, COUNT(lt.word_id) AS nbOccurrences, w.word
FROM LingTask lt
	INNER JOIN Words w ON lt.word_id=w.id
	INNER JOIN Videos v ON lt.video_id=v.id
WHERE w.language="swe" AND v.videotype IN ('target') AND lt.role='*SUJ'
GROUP BY lt.word_id
ORDER BY w.word 
;


-- Word length
-- 20 longest words in db
SELECT word, LENGTH(word) AS length FROM Words ORDER BY length DESC LIMIT 20;
-- Longest word for each language:
--  Spanish
SELECT word, LENGTH(word) AS length FROM Words 
WHERE language="spa"
ORDER BY length DESC LIMIT 5;
-- Swedish
SELECT word, LENGTH(word) AS length FROM Words 
WHERE language="swe"
ORDER BY length DESC LIMIT 5;
-- Average length for each language



-- Problem: some words in the database end with a comma ',' or any other pattern which shows you that sth's wrong
-- Goal: try to see where these words come from (when are they populated into the db) to work on a solution
-- How many words in the database do end with a comma (but substitute with other unwanted pattern as well)?
SELECT COUNT(*) FROM Words WHERE word LIKE '%Vale%';
-- Query: 
SELECT w.id, w.word, p.name, lt.role, v.videoname
FROM LingTask lt
	INNER JOIN Words w ON lt.word_id=w.id
	INNER JOIN Videos v ON lt.video_id=v.id
	INNER JOIN Participant p ON lt.participant_id=p.id
WHERE w.word LIKE '%Vale%'
;



-- In order to save SQL output to csv format and put back output to standard
.echo off
.headers on
.nullvalue NULL
.mode csv
.output filename.csv
SELECT column FROM table;
.output stdout


