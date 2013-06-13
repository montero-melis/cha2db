/130419
/Data extraction, processing and populating of database
/G Montero-Melis


Outline
======

This document describes all the steps needed to go from the raw data (i.e. transcriptions in .cha format) to the desired output: a populated SQLite database.
The document describes how this is implemented by a series of programs in this repo.


Input: raw transcription data
========

Content
-------

The transcriptions contain descriptions of 40 different short cartoons showing a character that moves along different paths and landscapes, carrying along different objects.
Each description typically consists of one sentence of around 10 words. There are descriptions of 80 participants altogether, 40 native speakers of Spanish and 40 native speakers of Swedish. 
Each transcription is about 150 rows long (around 6 KB).


Form
----

The raw data consist of transcriptions that follow certain conventions. Concretely they follow the conventions of transcriptions in CHAT-format, as used in the [CHILDES project](http://childes.psy.cmu.edu/).

Every transcription consists of a **header** containing metadata about the transcription. This is a typical header:

	1     @Begin
	2     @Languages:	spa
	3     @Participants:	SUJ Spanish_Native_216 Target_Adult, EXP Guillermo
	4     	Investigator
	5     @ID:	spa|motion|SUJ||male|SpAD||Target_Adult||
	6     @ID:	spa|motion|EXP||male|||Investigator||
	7     @Transcriber:	guillermo
	8     @Media:	Popi_SP_216_ord2, audio
	9     @Comment:	Order 2

Some but not all of the information in the header has to be extracted by the program.
More on that below.

Then comes the **body** of the transcription. Here is an example:

	18    @G:	tgt_cherue
	19    *EXP:	Popi un balancín una calle .
	20    *EXP:	qué ha ocurrido ? 
	21    *SUJ:	&k tirando de un balancín cruza: la calle . 
	22    @G:	pre_pnegro
	23    *SUJ:	empuja la rueda hacia la cueva . 
	25    @G:	trd_brocol
	26    *SUJ:	baja la carretilla por la montaña . 
	

The lines beginning with `@G` announce that a new video is being described. 
The string that follows these lines (e.g. `tgt_cherue`, l.18) is the ID of the video.
The three letter code `*EXP:` or `*SUJ:` indicates who is talking, either the experimenter or the participant ("subject").


Output: database in SQLite format
======================

The desired output is a SQLite database.
Eventually, the objects that we will analyze will often be data matrices for each individual transcription, or combinations of several matrices for different groupings according to certain criteria. 
For example, we may wish to collapse all data matrices for the Spanish speakers, or all the matrices for women, or all of those who carried out the tasks in a certain order. 
We refer to the data that will mainly be analysed as **data proper**, while the information that will be used in order to group data from different source we call **metadata**. 
The former is contained in the body of the transcriptions, the latter in the headers.
We find that the most efficient way to organise this data is in database format

For analysis purposes the data will be organized in a term-by-videoclip matrix.
To illustrate such a matrix, this is what it would look like for the data above:

	+-------------+------------+------------+------------+
	|             | tgt_cherue | pre_pnegro | trd_brocol |
	+-------------+------------+------------+------------+
	| tirando     |          1 |          0 |          0 |
	| de          |          1 |          0 |          0 |
	| un          |          1 |          0 |          0 |
	| balancín    |          1 |          0 |          0 |
	| cruza       |          1 |          0 |          0 |
	| la          |          1 |          2 |          2 |
	| calle       |          1 |          0 |          0 |
	| empuja      |          0 |          1 |          0 |
	| rueda       |          0 |          1 |          0 |
	| hacia       |          0 |          1 |          0 |
	| cueva       |          0 |          1 |          0 |
	| baja        |          0 |          0 |          1 |
	| carretilla  |          0 |          0 |          1 |
	| por         |          0 |          0 |          1 |
	| montaña     |          0 |          0 |          1 |
	+-------------+------------+------------+------------+

This is the kind of representation we typically will be working on. However, once normalised, the database will not store the information in that way. More on that in the next section.


Database structure
=================

Tables
------

	Condition     Gender        PartGroup     Videos      
	DescrMatrix   Interaction   Participant   Words       
	Experimenter  Language      Profile    


Schema
------

	CREATE TABLE Language (id INTEGER PRIMARY KEY, language TEXT);
	CREATE TABLE Gender (id INTEGER PRIMARY KEY, gender TEXT);
	CREATE TABLE PartGroup (id INTEGER PRIMARY KEY, partGroup TEXT);
	CREATE TABLE Profile (id INTEGER PRIMARY KEY, profile TEXT);
	CREATE TABLE Condition (id INTEGER PRIMARY KEY, condition TEXT);
	CREATE TABLE Videos (id INTEGER PRIMARY KEY, videoname TEXT, videotype TEXT);
	CREATE TABLE Words (id INTEGER PRIMARY KEY, word TEXT, language_id INTEGER);
	CREATE TABLE Experimenter(
	        id INTEGER PRIMARY KEY,
	        name TEXT,
	        gender_id INTEGER,
	        L1 INTEGER,
	        FOREIGN KEY(gender_id) REFERENCES Gender(id),
	        FOREIGN KEY(L1) REFERENCES Language(id)
	        );
	CREATE TABLE Participant(
	        id INTEGER PRIMARY KEY,
	        name TEXT,
	        gender_id INTEGER,
	        L1 INTEGER,
	        partGroup_id INTEGER,
	        age REAL,
	        OQPTscore REAL,
	        FOREIGN KEY(gender_id) REFERENCES Gender(id),
	        FOREIGN KEY(L1) REFERENCES Language(id)
	        );
	CREATE TABLE Interaction(
	        id INTEGER PRIMARY KEY,
	        participant_id INTEGER,
	        experimenter_id INTEGER,
	        language_id INTEGER,
	        orderLing INTEGER,
	        profile_id INTEGER,
	        condition_id INTEGER,
	        transcriber TEXT,
	        FOREIGN KEY(participant_id) REFERENCES Participant(id), 
	        FOREIGN KEY(experimenter_id) REFERENCES Experimenter(id),    
	        FOREIGN KEY(language_id) REFERENCES Language(id),  
	        FOREIGN KEY(profile_id) REFERENCES Profile(id),
	        FOREIGN KEY(condition_id) REFERENCES Condition(id)
	        );
	CREATE TABLE DescrMatrix(
	        interaction_id INTEGER,
	        video_id INTEGER,
	        role TEXT,
	        word_id INTEGER
	        );


Steps
=====

The steps to get from the raw data to the data matrices are:

1. Extraction of metainformation (headers) and data proper (body)
2. Data processing: remove noise from the data
3. Conversion into right format: tuples and dictionaries
4. Populate database
5. Check output, make necessary corrections uin 2. and 3.



1.  Extraction
============


The basic extraction (or unpickeling) of the data is done by the `CHAunpickle.py` code for Python (see in shared Dropbox folder).
It is not perfect for the task and needs changes, but it does the basic job.
The problem now is that it extracts too much information, but since the files are so lite, this might not even be a problem. In other words, it might be the right approach to extract *everything* first, and then to get rid of the unwanted information.

This is how it works just now. Let this be a sample input:

	1     @Begin
	2     @Languages:	spa
	3     @Participants:	SUJ Spanish_Native_418 Target_Adult, EXP Guillermo
	4     	Investigator
	5     @ID:	spa|motion|SUJ||male|SpAD||Target_Adult||
	6     @ID:	spa|motion|EXP||male|||Investigator||
	7     @Transcriber:	guillermo
	8     @Media:	Popi_SP_418_ord3, audio
	9     @Comment:	Ord3
	10    @G:	prt_meuche
	11    @G:	tgm_sactoi
	12    *EXP:	aquí esta Popi .
	13    *EXP:	hay un saco .
	14    *EXP:	hay un tejado . 
	15    *EXP:	qué ha ocurrido ? 
	16    *SUJ:	pues Popi ha subido (.) un saco (.) eh por: la ladera de un tejado
	17    	hasta la punta de su casa . 
	18    @G:	prt_rourue
	19    *EXP:	Popi de nuevo .
	20    *EXP:	una rueda, una calle . 
	21    *EXP:	qué ha ocurrido ? 
	22    *SUJ:	Popi ha cruzado una calle rodando una rueda de carro . 
	23    @G:	trd_brocol
	24    *SUJ:	Popi ha bajado la ladera de una montaña (.) hm (.) estirando de una
	25    	carretilla . 

Then this is the corresponding output from `CHAunpickle.py`:

	[   ('@Languages', 'spa'),
	    (   '@Participants',
	        'SUJ Spanish_Native_418 Target_Adult, EXP Guillermo Investigator'),
	    ('@ID', 'spa|motion|SUJ||male|SpAD||Target_Adult||'),
	    ('@ID', 'spa|motion|EXP||male|||Investigator||'),
	    ('@Transcriber', 'guillermo'),
	    ('@Media', 'Popi_SP_418_ord3, audio'),
	    ('@Comment', 'Ord3'),
	    ('@G', 'prt_meuche'),
	    ('@G', 'tgm_sactoi'),
	    ('*EXP', 'aquxc3\xad esta Popi .'),
	    ('*EXP', 'hay un saco .'),
	    ('*EXP', 'hay un tejado .'),
	    ('*EXP', 'quxc3\xa9 ha ocurrido ?'),
	    (   '*SUJ',
	        'pues Popi ha subido (.) un saco (.) eh por: la ladera de un tejado hasta la punta de su casa .'),
	    ('@G', 'prt_rourue'),
	    ('*EXP', 'Popi de nuevo .'),
	    ('*EXP', 'una rueda, una calle .'),
	    ('*EXP', 'quxc3\xa9 ha ocurrido ?'),
	    ('*SUJ', 'Popi ha cruzado una calle rodando una rueda de carro .'),
	    ('@G', 'trd_brocol'),
	    (   '*SUJ',
	        'Popi ha bajado la ladera de una montaxc3\\xb1a (.) hm (.) estirando de una carretilla .')]


Now, we can consider in more detail what information has to be extracted and what problems there are so far.

Metainformation
---------------

Regarding the metainformation (lines 1--9 in the example above), the following is relevant information:

- *Language*: the three letter code following `@Languages`. Here "spa".
- *Paricipant*: Not the whole of the line `@Participants` is needed, but only the string between  `SUJ` and `EXP`. In the example above this would be "Spanish_Native_418 Target_Adult"
- *Gender*: first `@ID` line, entry before the 5th pipe ("|"). Here, "male".
- *Group*: first `@ID` line, entry before the 6th vertical bar `|`. Here, "SpAD"
- *Animation order*: Entry in first `@Comment` field. Here, "Ord3".
- *Task order*: This has yet to be included in the transcriptions, but it will be the information contained in a second `@Comment` field.


Body (data proper)
-----------------

As it is now `CHAUnpicke.py` extracts unnecessary information, since the speech by the experimenter is not needed. 
The speech of the experimenter corresponds to all lines beginning with `*EXP`. 
However, even if this part of the transcriptions will not be analyzed now, it would be nice to keep in mind that one might want to analyse it at a later moment.
Therefore, it should not be made too difficult to change the code later in order to include the experimenter's speech. 

A **major problem** in this step is that non-standard characters like accents or `ñ` are wrongly rendered.
This has to be solved.



2. Data processing
=================

Now we want to remove noise and other unwanted characteristics of the transcription data.



Filling sounds and words with no (interesting) content
-----------

Sounds like "eh", "hmm" and so on have to be removed.
Also words whose meaning is not in any way relevant, like "and", "or" etc.
The best way to solve this is probably by making an explicit list of all words to be excluded.


Repetitions and retracings
--------------------------

Often speakers repeat a word, correct what they just said and so on. All of these features of normal speech are coded in the transcription.
In principle, we want to be able to remove them. But there are cases where we might want to compare the result of removing them or not.

Here is an example of a **repetition** (marked with "[/]"):

	*SUJ:	sube con [/] con el coche por una duna (.) por la playa . 

In this case we want to remove the word that precedes the string `[/]` (i.e. "con").

By default, the scope of the repetition symbol `[/]` is the preceding symbol. But if several words are repeated, the scope is marked by brackets `<i am scoped>`, as in the following example:

	*EXP:	la: [/] la de <lo que ocurre> [/] (.) lo que ocurre en la acción . 

In this case we eant to remove everything within the brackets, the brackets included.

**Retracings** are marked in a similar way, as here:

	*SUJ:	sube el tejado <llevando el flotador> [//] empujando el flotador . 

The same idea of scope applies as in repetitions.

Once we have treated repetitions and retracings as we want (either by removing them or keeping them), we have to remove the `[\]` or `[\\]` string.


Punctuation marks and other symbols
------------------------

We want to remove all punctuation marks at the end of a sentence, like "?"" and ".".
Likewise we want to remove colons (":"), which mark lengthenings of a vowel, and the string "(.)" which signifies a pause.



Allomorphs
----------

Sometimes the same word might be spelled in different ways (e.g. Swedish "neråt" and "nedåt"). Similar things can happen if a word is sometimes spelled with an initial capital.
We want to make sure that different spellings for the same word get collapsed into the same category.
This will probably have to be solved by using regular expressions on all words contained in some list. The list can be established by looking at the output of the program and noting unwanted categories.



3. Conversion into right format
==============================

In order to convert the data into matrix form, we first have to obtain the right tuples.


Metadata
--------

I am not sure how the metadata ought to be stored. 
It certainly doesn't need to be part of the matrix, since we only want to use it in order to group different matrices.
But if having them in the matrix were the most logical way to store the information, then that's how it should be...

One thing to keep in mind is that one might want to make this metadata readable in R. That would make it possible to collapse matrices in R. Of course, another possibility is to do the matrix operations in Python and then export them to R.


Body
----

For the transcription body as exemplified above, we want to obtain the following tuples (NB: The processing step described in 2. has not been applied):

	[   
	    ('tgm_sactoi', 'pues Popi ha subido (.) un saco (.) eh por: la ladera de un tejado hasta la punta de su casa .'),
	    ('prt_rourue', 'Popi ha cruzado una calle rodando una rueda de carro .'),
	    (   'trd_brocol', 'Popi ha bajado la ladera de una montaxc3\\xb1a (.) hm (.) estirando de una carretilla .')]


The matrix will then be obtained by counting in which of the video context each of the words appear (see section Output: data matrices)


4. Populate database
====================

Here comes text replacing "Conversion into matrix form"


4. Conversion into matrix form (SECTION NOT NEEDED ANYMORE!)
=============================

The matrix form is only one step away. The algorithm might look something like this:

1. Establish a list of the N unique words by counting only once all words that appear on the right-hand side of the tuples obtained in step 3
2. Establish a list of all the different videoclips (i.e. the strings on the left field of the tuples)
3. For each videoclip create a vector containing N zeroes.
4. For each videoclip go through the description (right-hand side) and count +1 for each word that matches the list from 1.

The matrices should be exported into a readable format e.g. CSV.



5. Necessary adjustments and corrections 
==========================================

This will replace "Combine different matrices"


5. Combine different matrices (SECTION NOT NEEDED ANYMORE!)
===========================

When we add matrices what will change -- apart from the frequency counts in the cells -- are the unique words, that is, the rows of the matrix. A new word will add a new row with its corresponding row label.
The column labels will be the same since all participants describe the same videoclips.

In order to combine matrices, two things have to be done. Let's say that a matrix B has to be combined with a matrix A. Then for each word in B,

1. If: the word is already present in the matrix A, then: add the corresponding row vector of B to that of A.
2. Else: append the corresponding row vector to the matrix.




