import os
import sqlite3

DB = "cha.db"

os.remove(DB)
conn = sqlite3.connect(DB)

c = conn.cursor()

# 1. Schema

c.execute('''CREATE TABLE IF NOT EXISTS language (id INTEGER PRIMARY KEY, language TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS experimenter (id INTEGER PRIMARY KEY, name TEXT, L1 INTEGER)''')

# 2. Inserts SQL statements

m = {   'exp_gender': 'male',
    'exp_name': 'Guillermo',
    'lang_interact': 'spa',
    'order': '4',
    'ppt_gender': 'female',
    'ppt_group': 'SpAD',
    'ppt_name': 'Spanish_Native_119',
    'ppt_role': 'Target_Adult',
    'transcr': 'guillermo'}

c.execute('SELECT id FROM language WHERE language = ?', (m["lang_interact"],))
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
   
# and so forth...
