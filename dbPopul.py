import os
import sqlite3

DB = "cha.db"

try:
    os.remove(DB)
except:
    print "Couldn't delete database"
    
conn = sqlite3.connect(DB)
c = conn.cursor()

## 1. Schema

# Tables created for normalization
c.execute('''CREATE TABLE IF NOT EXISTS language (id INTEGER PRIMARY KEY, lang TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS gender (id INTEGER PRIMARY KEY, gen TEXT)''') #TODO: decide whether gender is INTEGER or TEXT
c.execute('''CREATE TABLE IF NOT EXISTS profile (id INTEGER PRIMARY KEY, prof TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS condition (id INTEGER PRIMARY KEY, cond TEXT)''')

# Tables for look-up
c.execute('''CREATE TABLE IF NOT EXISTS experimenter 
    (id INTEGER PRIMARY KEY, name TEXT, L1 INTEGER, gender INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS interaction 
    (id INTEGER PRIMARY KEY, nameParticipant INTEGER, langInteraction INTEGER, orderLing INTEGER, profile INTEGER, condition INTEGER)''')

## 2. Inserts SQL statements

m = {   'exp_gender': 'male',
    'exp_name': 'Guillermo',
    'lang_interact': 'spa',
    'order': '4',
    'ppt_gender': 'female',
    'ppt_group': 'SpAD',
    'ppt_name': 'Spanish_Native_119',
    'ppt_role': 'Target_Adult',
    'transcr': 'guillermo'}


# Info for 'experimenter' table
c.execute('INSERT INTO experimenter VALUES (NULL, ?, NULL, ?)', (m["exp_name"],m["exp_gender"])) #TODO: decide whether gender is INTEGER or TEXT

# 'interaction' table
c.execute('SELECT id FROM language WHERE lang = ?', (m["lang_interact"],))
row = c.fetchone()
if row is not None:
    id_lang_interact = row[0]
else:
    c.execute('INSERT INTO language VALUES (NULL, ?)', (m["lang_interact"],))
    id_lang_interact = c.lastrowid    
   

c.execute('SELECT id FROM experimenter WHERE name = ?', (m["exp_name"],))
row = c.fetchone()
if row is not None:
    id_experimenter = row[0]
else:
    c.execute('INSERT INTO experimenter VALUES (NULL, ?, ?)', (m["exp_name"], id_lang_interact))
    id_experimenter = c.lastrowid


conn.commit()
conn.close()
