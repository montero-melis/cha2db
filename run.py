from CHAparse import *
from dbPopul import *
from os import *
import re
import sqlite3



# # Delete and create anew until the function works as expected
try:
    os.remove("cha_test.db")
except:
    print "Couldn't delete database"


# Populate db with participant data:
dbPopul("cha_test.db", "participant_data_140117.txt")


# Populate with linguistic data from all .cha files in directory
for eachfile in os.listdir(os.getcwd()):
    if eachfile.endswith(".cha"):
    	print eachfile
        dbPopul("cha_test.db", None, CHA(eachfile).parse_meta(), CHA(eachfile).process_body())


# # With individual file (for testing or adding)
# dbPopul(
# 	"cha_test.db",	# name of dB
# 	"data_hopi.txt",	# file with participant info
# 	CHA("SwAD_1004_pop_or1_ori.cha").parse_meta(),	# metainformation extrcted from transcription
# 	CHA("SwAD_1004_pop_or1_ori.cha").process_body()	# body of transcription extracted and processed
# 	)


########################################
########################################

## Certain information has to be included 'manually'
conn = sqlite3.connect("cha_test.db")
c = conn.cursor()

# videos.videotype has four possible values: 'target', 'training', 'distractor', 'closing'
videos = []
rows = c.execute('''SELECT videoname FROM Videos''')
for row in rows:
    videos.append(row[0])
    
for videoname in videos:
    if videoname == 'prt_meuche':
        vtype = 'training'
    elif re.match('dis', videoname):
        vtype = 'distractor'
    elif videoname == 'closing':
        vtype = 'closing'
    else:
        vtype = 'target'
        
    c.execute("UPDATE Videos SET videotype=? WHERE videoname=?", (vtype, videoname))

conn.commit()
conn.close()
