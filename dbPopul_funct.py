import os
import sqlite3
import CHAparse

def dbPopul(dbName, metainfo, body):

    DB = dbName

    # # Delete and create anew until the function works as expected
    # try:
    #     os.remove(DB)
    # except:
    #     print "Couldn't delete database"
        
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    ## 1. Schema

    # Table names begin with Capital Letter
    # Variable names written with small caps

    # Tables created for normalization (look-up)
    c.execute('''CREATE TABLE IF NOT EXISTS Language (lang_id INTEGER PRIMARY KEY, language TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS Gender (gend_id INTEGER PRIMARY KEY, gender TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS PartGroup (group_id INTEGER PRIMARY KEY, partGroup TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS Profile (prof_id INTEGER PRIMARY KEY, profile TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS Condition (cond_id INTEGER PRIMARY KEY, condition TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS Videos (video_id INTEGER PRIMARY KEY, videoname TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS Words (word_id INTEGER PRIMARY KEY, word TEXT, language INTEGER)''')


    ## Tables with interesting relations

    # Experimenter
    c.execute('''CREATE TABLE IF NOT EXISTS Experimenter(
        expe_id INTEGER PRIMARY KEY,
        name TEXT,
        gender INTEGER,
        L1 INTEGER,
        FOREIGN KEY(gender) REFERENCES Gender(gend_id),
        FOREIGN KEY(L1) REFERENCES Language(lang_id)
        )'''
    )

    # Participant
    c.execute('''CREATE TABLE IF NOT EXISTS Participant(
        part_id INTEGER PRIMARY KEY,
        name TEXT,
        gender INTEGER,
        L1 INTEGER,
        partGroup INTEGER,
        age REAL,
        OQPTscore INTEGER,
        FOREIGN KEY(gender) REFERENCES Gender(gend_id),
        FOREIGN KEY(L1) REFERENCES Language(lang_id)
        )'''
    )

    # Interaction
    c.execute('''CREATE TABLE IF NOT EXISTS Interaction(
        inte_id INTEGER PRIMARY KEY,
        partName INTEGER,
        expeName INTEGER,
        langInteraction INTEGER,
        orderLing INTEGER,
        profile INTEGER,
        condition INTEGER,
        FOREIGN KEY(partName) REFERENCES Participant(part_id),    
        FOREIGN KEY(expeName) REFERENCES Experimenter(expe_id),    
        FOREIGN KEY(langInteraction) REFERENCES Language(lang_id),  
        FOREIGN KEY(profile) REFERENCES Profile(prof_id),
        FOREIGN KEY(condition) REFERENCES Condition(cond_id)
        )'''
    )

    # DescrMatrix
    c.execute('''CREATE TABLE IF NOT EXISTS DescrMatrix(
        interaction INTEGER,
        video INTEGER,
        role TEXT,
        word INTEGER
        )'''
    )



    ## 2. Inserts SQL statements

    m = metainfo
    t = body

    ## Experimenter table and indexes -- add only a row to this table if new experimenter!
    # Check experimenter name
    c.execute('SELECT expe_id FROM Experimenter WHERE name = ?', (m["exp_name"],))
    row = c.fetchone()
    if row is not None: # that is if experimenter already in db
        expe_name_id = row[0]
    else: # experimenter is not in the db
        c.execute('SELECT gend_id FROM Gender WHERE gender = ?', (m["exp_gender"],)) # fetch gender
        row = c.fetchone()
        if row is not None: # value for gender is already in db
            expe_gender_id = row[0]
        else: # value for gender is not in db and has to be added
            c.execute('INSERT INTO Gender VALUES (NULL,?)', (m["exp_gender"],))
            expe_gender_id = c.lastrowid
        c.execute('INSERT INTO Experimenter VALUES (NULL,?,?,NULL)', (m["exp_name"],expe_gender_id)) # populate Experimenter table
        expe_name_id = c.lastrowid


    ## Participant table and indexes
    # participant gender
    c.execute('SELECT gend_id FROM Gender WHERE gender = ?', (m["ppt_gender"],))
    row = c.fetchone()
    if row is not None:
        part_gender_id = row[0]
    else:
        c.execute('INSERT INTO Gender VALUES (NULL,?)', (m["ppt_gender"],))
        part_gender_id = c.lastrowid
    # participant group
    c.execute('SELECT group_id FROM PartGroup WHERE partGroup = ?', (m["ppt_group"],))
    row = c.fetchone()
    if row is not None:
        part_group_id = row[0]
    else:
        c.execute('INSERT INTO PartGroup VALUES (NULL,?)', (m["ppt_group"],))
        part_group_id = c.lastrowid
    # participant name
    part_name = m["ppt_name"]
    # participant role: not inserted into db since this info is alread covered as 'participant group'
    # populate Participant table
    c.execute('INSERT INTO Participant VALUES (NULL,?,?,NULL,?,NULL,NULL)', (part_name, part_gender_id, part_group_id))
    part_name_id = c.lastrowid


    ## Interaction table
    # language of interaction
    c.execute('SELECT lang_id FROM Language WHERE language = ?', (m["lang_interact"],))
    row = c.fetchone()
    if row is not None:
        interaction_lang_id = row[0]
    else:
        c.execute('INSERT INTO Language VALUES (NULL, ?)', (m["lang_interact"],))
        interaction_lang_id = c.lastrowid    
    # orderLing (order in which linguistic task is performed)
    orderLing = m["order"]
    # Populate Interaction table
    c.execute('INSERT INTO Interaction VALUES (NULL,?,?,?,?,NULL,NULL)', (part_name_id, expe_name_id, interaction_lang_id, orderLing))
    interaction_id = c.lastrowid

    ## DescrMatrix table
    for turn in t: # Each turn refers to what each participant (subject, experimenter) says for each description
        # Parse video (turn[0]), enter it to Videos if necessary, and keep its id as a variable video_id
        c.execute('SELECT video_id FROM Videos WHERE videoname = ?', (turn[0],))
        row = c.fetchone()
        if row is not None:
            video_id = row[0]
        else:
            c.execute('INSERT INTO Videos VALUES (NULL, ?)', (turn[0],))
            video_id = c.lastrowid    
        # Update variable 'role' with value turn[1]
        role = turn[1]
        # For each word in turn[2] (use split method!):
        for eachword in turn[2].split():
            # Parse each word, enter into Words if necessary, keep it id as variable word_id
            c.execute('SELECT word_id FROM Words WHERE word = ? AND language = ?', (unicode(eachword, 'utf-8'), interaction_lang_id))
            row = c.fetchone()
            if row is not None:
                word_id = row[0]
            else:
                c.execute('INSERT INTO Words VALUES (NULL, ?, ?)', (unicode(eachword, 'utf-8'), interaction_lang_id))
                word_id = c.lastrowid    
            # Insert into DescrMatrix : (inte_id, video_id, role, )
            c.execute('INSERT INTO DescrMatrix VALUES (?,?,?,?)', (interaction_id, video_id, role, word_id))


    conn.commit()
    conn.close()
