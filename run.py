from CHAparse import *
from dbPopul_funct import *
print CHA("SpAD_119_pop_or4_ori.cha").parse_meta()
print CHA("SpAD_119_pop_or4_ori.cha").process_body()
dbPopul("test.db",CHA("SpAD_119_pop_or4_ori.cha").parse_meta(), CHA("SpAD_119_pop_or4_ori.cha").process_body())
