library("RSQLite")

setwd("C:/Documents and Settings/gumo8029/Mina dokument/gitRepos/hopiAnalysesR")

con <- dbConnect(drv="SQLite", dbname = "cha.db")
## list all tables
tables <- dbListTables(con)

dm <- dbGetQuery(conn=con, 
           statement=paste("SELECT * FROM DescrMatrix
                           WHERE role='*SUJ' AND  ")
                 )
