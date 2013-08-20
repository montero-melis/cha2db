## This script creates documents that serve as input to the 'textmatrix' function in the R package 'lsa'
import os
import sqlite3
import codecs

conn = sqlite3.connect('cha.db')
c = conn.cursor()

results = c.execute('''SELECT p.name, v.videoname, w.word, w.language
  FROM Participant p 
    INNER JOIN LingTask lt ON lt.participant_id=p.id 
    INNER JOIN Videos v ON lt.video_id=v.id
    INNER JOIN Words w ON w.id=lt.word_id
  WHERE lt.role='*SUJ' AND v.videotype IN ('target') AND w.language ='spa' 
  ''') # for now, change 'swe' to 'spa' to get docs in one or the other lanugage

# Create one document per videoclip and language, using the data for all participants of that language
files_dict = {}

def get_fd(files_dict,videoname, lang):
    if videoname not in files_dict:
        files_dict[videoname] = {}
        files_dict[videoname] = codecs.open("%s_%s.txt" % (lang,videoname), "w", "utf-8")
        
    return files_dict[videoname]

for r in results:
    _, videoname, word, lang = r
    f = get_fd(files_dict, videoname, lang)
    f.write("%s " % (word,))
    print files_dict



# # Create one document per videoclip and participant

# files_dict = {}

# def get_fd(files_dict,name,videoname):
#     if name not in files_dict:
#         files_dict[name] = {}
#     if videoname not in files_dict[name]:
#         files_dict[name][videoname] = codecs.open("%s_%s.txt" % (name,videoname), "w", "utf-8")
        
#     return files_dict[name][videoname]

# for r in results:
#     name, videoname, word = r
#     f = get_fd(files_dict, name, videoname)
#     f.write("%s/" % (word,))

# # close all files
# [f.close() for f in files_dict] # Apparently no file closing is needed when using the codecs.open() method


conn.commit()
conn.close()
