## Set working directory
# setwd("/home/guille/Documents/thesis/cha2db/")

library("RSQLite")
library("reshape")
library("lsa")

m <- dbDriver("SQLite")
con <- dbConnect(m, dbname = "cha.db")

# sample data
sample <- dbGetQuery(con, "-- Data to convert into matrix
  SELECT p.name, v.videoname, w.word
  FROM DescrMatrix dm
    INNER JOIN Words w ON dm.word_id=w.id
  	INNER JOIN Videos v ON dm.video_id=v.id
  	INNER JOIN Interaction i ON dm.interaction_id=i.id
  	INNER JOIN Participant p ON i.participant_id=p.id
  WHERE dm.role='*SUJ'
  LIMIT 200
")

book.sales = read.csv("http://news.mrdwab.com/data-booksales")

sample$name <- as.factor(sample$name)
sample$videoname <- as.factor(sample$videoname)
sample$word <- as.factor(sample$word)

m.sample <- melt(sample, id.vars=1:3)
 cast(sample, ... ~ videoname)