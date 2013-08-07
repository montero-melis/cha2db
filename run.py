from CHAparse import *
from dbPopul import *
from os import *
import re


# Delete and create anew until the function works as expected
try:
    os.remove("testdb.db")
except:
    print "Couldn't delete database"


# Populate db with participant data:
dbPopul("testdb.db", "data_hopi.txt")


# Populate with linguistic data from all .cha files in directory
for eachfile in os.listdir(os.getcwd()):
    if eachfile.endswith(".cha"):
    	print eachfile
        dbPopul("testdb.db", None, CHA(eachfile).parse_meta(), CHA(eachfile).process_body())




# # With individual file (for testing)
# dbPopul(
# 	"testdb.db",	# name of dB
# 	"data_hopi.txt",	# file with participant info
# 	CHA("SwAD_1004_pop_or1_ori.cha").parse_meta(),	# metainformation extrcted from transcription
# 	CHA("SwAD_1004_pop_or1_ori.cha").process_body()	# body of transcription extracted and processed
# 	)
