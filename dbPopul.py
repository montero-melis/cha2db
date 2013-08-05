import os
import sqlite3
import csv
import CHAparse


def dbPopul(dbName, subject_info=None, ling_data=None, nonling_data=None):

    DB = dbName

    # Delete and create anew until the function works as expected
    try:
        os.remove(DB)
    except:
        print "Couldn't delete database"
        
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
    		subj_data = csv.reader(csvfile)
    		for row in subj_data:
    			print row


    # data from linguistic task

    if ling_data is None:
    	print "No linguistic data provided"
    # else:


    # data from nonlinguistic task

    if nonling_data is None:
    	print "No nonlinguistic data provided"
    # else:



    # m = metainfo
    # t = body

    # ## Experimenter table and indexes -- add only a row to this table if new experimenter!
    # # Check experimenter name
    # c.execute('SELECT id FROM Experimenter WHERE name = ?', (m["exp_name"],))
    # row = c.fetchone()
    # if row is not None: # that is if experimenter already in db
    #     expe_name_id = row[0]
    # else: # experimenter is not in the db
    #     c.execute('SELECT id FROM Gender WHERE gender = ?', (m["exp_gender"],)) # fetch gender
    #     row = c.fetchone()
    #     if row is not None: # value for gender is already in db
    #         expe_gender_id = row[0]
    #     else: # value for gender is not in db and has to be added
    #         c.execute('INSERT INTO Gender VALUES (NULL,?)', (m["exp_gender"],))
    #         expe_gender_id = c.lastrowid
    #     c.execute('INSERT INTO Experimenter VALUES (NULL,?,?,NULL)', (m["exp_name"],expe_gender_id)) # populate Experimenter table
    #     expe_name_id = c.lastrowid


    # ## Participant table and indexes
    # # participant gender
    # c.execute('SELECT id FROM Gender WHERE gender = ?', (m["ppt_gender"],))
    # row = c.fetchone()
    # if row is not None:
    #     part_gender_id = row[0]
    # else:
    #     c.execute('INSERT INTO Gender VALUES (NULL,?)', (m["ppt_gender"],))
    #     part_gender_id = c.lastrowid
    # # participant group
    # c.execute('SELECT id FROM PartGroup WHERE partGroup = ?', (m["ppt_group"],))
    # row = c.fetchone()
    # if row is not None:
    #     part_group_id = row[0]
    # else:
    #     c.execute('INSERT INTO PartGroup VALUES (NULL,?)', (m["ppt_group"],))
    #     part_group_id = c.lastrowid
    # # participant name
    # part_name = m["ppt_name"]
    # # participant role: not inserted into db since this info is alread covered as 'participant group'
    # # populate Participant table
    # c.execute('INSERT INTO Participant VALUES (NULL,?,?,NULL,?,NULL,NULL)', (part_name, part_gender_id, part_group_id))
    # part_name_id = c.lastrowid


    # ## Interaction table
    # # language of interaction
    # c.execute('SELECT id FROM Language WHERE language = ?', (m["lang_interact"],))
    # row = c.fetchone()
    # if row is not None:
    #     interaction_lang_id = row[0]
    # else:
    #     c.execute('INSERT INTO Language VALUES (NULL, ?)', (m["lang_interact"],))
    #     interaction_lang_id = c.lastrowid    
    # # orderLing (order in which linguistic task is performed)
    # orderLing = m["order"]
    # # Transcriber
    # transcr = m["transcr"]
    # # Populate Interaction table
    # c.execute('INSERT INTO Interaction VALUES (NULL,?,?,?,?,NULL,NULL,?)', (part_name_id, expe_name_id, interaction_lang_id, orderLing, transcr))
    # interaction_id = c.lastrowid

    # ## DescrMatrix table
    # for turn in t: # Each turn refers to what each participant (subject, experimenter) says for each description
    #     # Parse video (turn[0]), enter it to Videos if necessary, and keep its id as a variable video_id
    #     c.execute('SELECT id FROM Videos WHERE videoname = ?', (turn[0],))
    #     row = c.fetchone()
    #     if row is not None:
    #         video_id = row[0]
    #     else:
    #         c.execute('INSERT INTO Videos VALUES (NULL, ?, NULL)', (turn[0],))
    #         video_id = c.lastrowid    
    #     # Update variable 'role' with value turn[1]
    #     role = turn[1]
    #     # For each word in turn[2] (use split method!):
    #     for eachword in turn[2].split():
    #         # Parse each word, enter into Words if necessary, keep it id as variable word_id
    #         c.execute('SELECT id FROM Words WHERE word = ? AND language_id = ?', (eachword, interaction_lang_id))
    #         row = c.fetchone()
    #         if row is not None:
    #             word_id = row[0]
    #         else:
    #             c.execute('INSERT INTO Words VALUES (NULL, ?, ?)', (eachword, interaction_lang_id))
    #             word_id = c.lastrowid    
    #         # Insert into DescrMatrix : (inte_id, video_id, role, )
    #         c.execute('INSERT INTO DescrMatrix VALUES (?,?,?,?)', (interaction_id, video_id, role, word_id))


    conn.commit()
    conn.close()

