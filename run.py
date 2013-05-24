from CHAparse import *
from dbPopul_funct import *
from os import *

for files in os.listdir(os.getcwd()):
    if files.endswith(".cha"):
        dbPopul("cha.db",CHA(files).parse_meta(), CHA(files).process_body())

