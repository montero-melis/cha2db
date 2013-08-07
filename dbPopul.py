import os
import sqlite3
import csv
import CHAparse
import re


def dbPopul(dbName, subject_info=None, ling_meta=None, ling_data=None, nonling_data=None):

    DB = dbName

    # # Delete and create anew until the function works as expected
    # try:
    #     os.remove(DB)
    # except:
    #     print "Couldn't delete database"
        
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    ## 1. Create db schema (if not exists)

    # Table names begin with Capital Letter
    # Variable names written with small caps

    # Participant
    c.execute('''CREATE TABLE IF NOT EXISTS Participant(
        id INTEGER PRIMARY KEY,
        name TEXT,
        groupname TEXT,
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
        )'''
    )

    # Linguistic task
    c.execute('''CREATE TABLE IF NOT EXISTS LingTask(
        participant_id INTEGER,
        video_id INTEGER,
        role TEXT,
        word_id INTEGER,
        FOREIGN KEY (participant_id) REFERENCES Participant(id),
        FOREIGN KEY (video_id) REFERENCES Video(id),
        FOREIGN KEY (word_id) REFERENCES Words(id)
        )'''
    )

    # Words
    c.execute('''CREATE TABLE IF NOT EXISTS Words (
    	id INTEGER PRIMARY KEY,
    	word TEXT,
    	language TEXT,
    	semantic_categ TEXT,
    	POS TEXT
    	)'''
    )

    # Videos (stimuli)
    c.execute('''CREATE TABLE IF NOT EXISTS Videos (id INTEGER PRIMARY KEY, videoname TEXT, videotype TEXT)''')

    # Nonlinguistic task
    c.execute('''CREATE TABLE IF NOT EXISTS NonlingTask (
        participant_id INTEGER,
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
    	)'''
    )


    ## 2. Insert SQL statements

    # Participant info

    if subject_info is None:
    	print "No participant info provided"
    else:
    	f = subject_info
    	with open(f) as csvfile:
            subj_data = csv.reader(csvfile, dialect='excel-tab')
            next(subj_data) # Don't want to include the header row
            for row in subj_data:
                uni_row = []
                for field in row:
                    uni_row.append(unicode(field,'utf-8')) # this is needed to get strings into unicode
                c.execute('INSERT INTO Participant VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', uni_row)


    # data from linguistic task

    if ling_meta is None or ling_data is None:
    	print "No (or not sufficient) linguistic data provided"
    else:

        m = ling_meta # m for metadata
        t = ling_data # t for text

        # Find participant ID (the name and the language are the only metada used)
        part_name = m["ppt_name"] # has form 'Spanish_Native_323'
        print part_name
        reg_name = re.compile(r"(\d+)") # match one or more digits
        match = reg_name.search(part_name)
        part_name = match.group(1) # Now the name is correctly (323,) in tuple format 
        c.execute('SELECT id FROM Participant WHERE name=?', (part_name,)) # get participant's ID in dB
        row = c.fetchone()
        if row is None:
            print "participant", part_name ,"is not in dB!"
        else:
            participant_id = row[0] # Since we want to extract the value from the tuple
            print "This is participant", participant_id

        # Keep the language of the interaction as a variable to be used to populate LingTask table
        lang = m["lang_interact"]

        # Populate LingTask table
        for turn in t: # Each turn refers to what each participant (subject/experimenter) says for each description
            # Parse video (turn[0]), enter it to Videos if necessary, and keep its id as a variable video_id
            c.execute('SELECT id FROM Videos WHERE videoname = ?', (turn[0],))
            row = c.fetchone()
            if row is not None:
                video_id = row[0]
            else:
                c.execute('INSERT INTO Videos VALUES (NULL, ?, NULL)', (turn[0],))
                video_id = c.lastrowid    
            # Update variable 'role' with value turn[1]
            role = turn[1]
            # For each word in turn[2] (use split method!):
            for eachword in turn[2].split():
                # Parse each word, enter into Words if necessary, keep its id as the variable word_id
                c.execute('SELECT id FROM Words WHERE word = ? AND language = ?', (eachword, lang))
                row = c.fetchone()
                if row is not None:
                    word_id = row[0]
                else:
                    c.execute('INSERT INTO Words VALUES (NULL, ?, ?, NULL,NULL)', (eachword, lang))
                    word_id = c.lastrowid    
                # Insert into LingTask : (inte_id, video_id, role, )
                c.execute('INSERT INTO LingTask VALUES (?,?,?,?)', (participant_id, video_id, role, word_id))


    # data from nonlinguistic task

    if nonling_data is None:
        print "No nonlinguistic data provided"
    # else:


    conn.commit()
    conn.close()

