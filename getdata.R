library("RSQLite")

setwd("C:/Documents and Settings/gumo8029/Mina dokument/gitRepos/cha2db")

con <- dbConnect(drv="SQLite", dbname = "cha.db")

## list of all tables in db
tables <- dbListTables(con)

# get data matrix for Sw705, videos 2--7 (sample data for illustration)
dm705 <- dbGetQuery(conn=con, 
           statement=paste("SELECT p.name, v.videoname, w.word, l.language
  FROM DescrMatrix dm
    INNER JOIN Words w ON dm.word_id=w.id
    INNER JOIN Videos v ON dm.video_id=v.id
    INNER JOIN Interaction i ON dm.interaction_id=i.id
    INNER JOIN Participant p ON i.participant_id=p.id
    INNER JOIN Language l ON i.language_id=l.id
  WHERE dm.role='*SUJ' 
    AND v.id BETWEEN 2 AND 7
    AND l.language ='swe' 
    AND p.id=21 ")
)
                 
# get data matrix for all Swedish participants
dmSw <- dbGetQuery(conn=con, 
                    statement=paste("SELECT p.name, v.videoname, w.word, l.language
    FROM DescrMatrix dm
    INNER JOIN Words w ON dm.word_id=w.id
    INNER JOIN Videos v ON dm.video_id=v.id
    INNER JOIN Interaction i ON dm.interaction_id=i.id
    INNER JOIN Participant p ON i.participant_id=p.id
    INNER JOIN Language l ON i.language_id=l.id
    WHERE dm.role='*SUJ' 
    AND v.videoname NOT IN ('prt_meuche','closing')
    AND l.language ='swe' ")
)

# Get into terms-by-documents format
dm705.t <- table(dm705$word, dm705$videoname)
dmSw.t <- table(dmSw$word, dmSw$videoname)
# Produce table in latex format that fits into presentation
xtable(dm705.t[1:15,1:4])
xtable(dmSw.t[sample(nrow(dmSw.t), 15), sample(ncol(dmSw.t),4)])
