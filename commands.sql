.echo on
.mode column
.headers on
.nullvalue NULL

-- How many participants per language
SELECT groupname, COUNT(*) FROM Participant GROUP BY groupname;


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




-- In order to save SQL output to csv format and put back output to standard
.echo off
.headers on
.nullvalue NULL
.mode csv
.output filename.csv
SELECT column FROM table;
.output stdout


