from CHAparse import *
from dbPopul import *
from os import *


# Delete and create anew until the function works as expected
try:
    os.remove("cha.db")
except:
    print "Couldn't delete database"



# Run on all files
for files in os.listdir(os.getcwd()):
    if files.endswith(".cha"):
        dbPopul("cha.db",CHA(files).parse_meta(), CHA(files).process_body())


# # Run on a particular file
# dbPopul("cha113.db",CHA("SpAD_113_pop_or3_ori_INCOMPL.cha").parse_meta(), CHA("SpAD_113_pop_or3_ori_INCOMPL.cha").process_body())
