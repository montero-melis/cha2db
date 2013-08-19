cha2db
======

This repository contains a series of programs and scripts to feed data from the Hopi project into a database.
Python program (CHAparse.py): takes transcriptions in .cha format (see CHILDES project or TalkBank.org) as input, and outputs the relevant information in SQLite database format.

Short description of the individual programs:

CHAparse.py
-----------

Parses the transcriptions for the linguistic Popi task. Transcriptions follow CHILDES conventions and are in .cha format.
The output is a dictionary-type of structure for the metadata included in the transcriptions (i.e. the information in the header), and a list-type of structure for the body of the transcriptions. 
The list for the transcription-body is a list of lists having three entries: [videoname, role, word].
Role refers to either *SUJ (the participant) or *EXP (the experimenter).

dbPopul.py
----------

This program populates the database with three types of input:

1) the output from CHAparse.py (see above);
2) the participant data with all the background info about participants from a tab-separated file;
3) the output from the nonlinguistic task, which is a file from e-Prime converted to csv.


run.py
------

A script to execute the dbPopul.py program.


The database
----------

Here is the database schema followed by explanations of each of the table entries. The explanations are typed as comments, preceded by #:

	CREATE TABLE LingTask( # Data for linguistic task
	        participant_id INTEGER, # automatically generated by SQLite
	        video_id INTEGER,
	        role TEXT, # Either SUJ (participant) or EXP (experimenter)
	        word_id INTEGER,
	        FOREIGN KEY (participant_id) REFERENCES Participant(id),
	        FOREIGN KEY (video_id) REFERENCES Video(id),
	        FOREIGN KEY (word_id) REFERENCES Words(id)
	        );
	CREATE TABLE NonlingTask (  # Data for nonlinguistic task
	        participant_id INTEGER, # automatically generated by SQLite
	        ExpName
			ExpCondition TEXT,
			Incl_Excl TEXT,
			Name TEXT,
			SessionDateTime TEXT,
			Session_Lang TEXT,
			Language TEXT,
			RandomList TEXT,
			ProcBlock TEXT,
			Procedure_Trial TEXT,
			Trial TEXT,
			CategBlocks TEXT,
			CategBlocks_Sample TEXT,
			FamList TEXT,
			FamList_Sample TEXT,
			Vid_Famil TEXT,
			PlayTime_Fam TEXT,
			Running_Trial INTEGER,
			ViewTime_Train REAL,
			CategTime_Train REAL,
			ListTrain TEXT,
			X_Train REAL,
			Y_Train REAL,
			Series INTEGER,
			Vid_Train TEXT,
			LogSeries INTEGER,
			ViewTime REAL,
			CategTime REAL,
			Log_All66 INTEGER,
			X REAL,
			Y REAL,
			Vid_Categ TEXT,
	        FOREIGN KEY (participant_id) REFERENCES Participant(id)
	    	);
	CREATE TABLE Participant( # Background information for participants
	        id INTEGER PRIMARY KEY,  # automatically generated by SQLite
	        name TEXT, # e.g. '103'
	        groupname TEXT, # 'SpAD' or 'SwAD' for Spanish and Swedish adults respectively
	        gender TEXT,
	        age REAL,
	        date_time INTEGER,
	        condition TEXT,
	        ling_order INTEGER,
	        nonling_randomlist INTEGER,
	        screenshots_nonling TEXT,
	        OQPT_score REAL,
	        experimenter TEXT,
	        exclude INTEGER,
	        comments_general TEXT,
	        comments_Ling TEXT,
	        comments_Nonling TEXT
	        );
	CREATE TABLE Videos (id INTEGER PRIMARY KEY, videoname TEXT, videotype TEXT);
	CREATE TABLE Words (
	    	id INTEGER PRIMARY KEY,
	    	word TEXT,
	    	language TEXT,
	    	semantic_categ TEXT,
	    	POS TEXT
	    	);

