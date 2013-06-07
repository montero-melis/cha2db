import os
import sqlite3
import codecs

conn = sqlite3.connect('cha.db')
c = conn.cursor()

results = c.execute('''SELECT p.name, v.videoname, w.word, l.language
  FROM DescrMatrix dm
    INNER JOIN Words w ON dm.word_id=w.id
    INNER JOIN Videos v ON dm.video_id=v.id
    INNER JOIN Interaction i ON dm.interaction_id=i.id
    INNER JOIN Participant p ON i.participant_id=p.id
    INNER JOIN Language l ON i.language_id=l.id
  WHERE dm.role='*SUJ' AND l.language ='swe'
  ''')


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
    f.write("%s/" % (word,))
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
