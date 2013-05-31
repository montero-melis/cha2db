from CHAparse import *
from dbPopul import *
from os import *


# Delete and create anew until the function works as expected
try:
    os.remove("cha.db")
except:
    print "Couldn't delete database"



# Run on all files
for eachfile in os.listdir(os.getcwd()):
    if eachfile.endswith(".cha"):
    	print eachfile
        dbPopul("cha.db",CHA(eachfile).parse_meta(), CHA(eachfile).process_body())


# # Run on all .cha files individually and create a db for each file
# for eachfile in os.listdir(os.getcwd()):
#     if eachfile.endswith(".cha"):
#     	try:
# 		    os.remove("cha.db")
# 		except:
# 		    print "Couldn't delete database"

#         dbPopul("cha.db",CHA(eachfile).parse_meta(), CHA(eachfile).process_body())


# # Run on a particular file
# dbPopul("cha113.db",CHA("SpAD_113_pop_or3_ori_INCOMPL.cha").parse_meta(), CHA("SpAD_113_pop_or3_ori_INCOMPL.cha").process_body())
