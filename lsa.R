library('lsa')
library('xtable')
library('stats')
library('graphics')

# # Set working directory
# setwd("/home/guille/Documents/thesis/cha2db/")
setwd("C:\\Documents and Settings\\gumo8029\\Mina dokument\\gitRepos\\cha2db")

# create text matrix from Documents;
# each doc is the added descriptions for each videoclip of all participants
# Only training item ('prt_meuche') and 'closing' removed (i.e. distractors included)
sp.matrix <- textmatrix("C:\\Documents and Settings\\gumo8029\\Mina dokument\\hopi_docs_lsa_input\\docs_spa")
sw.matrix <- textmatrix("C:\\Documents and Settings\\gumo8029\\Mina dokument\\hopi_docs_lsa_input\\docs_swe")
all.matrix <- textmatrix("C:\\Documents and Settings\\gumo8029\\Mina dokument\\hopi_docs_lsa_input\\docs_all")
# matrix for a single participant, might come in handy for illustration
sw.705.matrix <- textmatrix("C:\\Documents and Settings\\gumo8029\\Mina dokument\\hopi_docs_lsa_input\\docs_swe705")

# same thing but only with target items (distractors also excluded)
sp.tgt.matrix <- textmatrix("C:\\Documents and Settings\\gumo8029\\Mina dokument\\hopi_docs_lsa_input\\docs_spa_target")
sw.tgt.matrix <- textmatrix("C:\\Documents and Settings\\gumo8029\\Mina dokument\\hopi_docs_lsa_input\\docs_swe_target")
all.tgt.matrix <- textmatrix("C:\\Documents and Settings\\gumo8029\\Mina dokument\\hopi_docs_lsa_input\\docs_all_target")

# Apply weighting schemes for each of the matrices above
# local weighting: log(type freq +1); global weighting: entropy
# matrices for all items
w.sp.matrix <- lw_logtf(sp.matrix)*gw_entropy(sp.matrix)
w.sw.matrix <- lw_logtf(sw.matrix)*gw_entropy(sw.matrix)
w.all.matrix <- lw_logtf(all.matrix)*gw_entropy(all.matrix)
# matrices for target items only
w.sp.tgt.matrix <- lw_logtf(sp.tgt.matrix)*gw_entropy(sp.tgt.matrix)
w.sw.tgt.matrix <- lw_logtf(sw.tgt.matrix)*gw_entropy(sw.tgt.matrix)
w.all.tgt.matrix <- lw_logtf(all.tgt.matrix)*gw_entropy(all.tgt.matrix)


# examples of related terms
nb.sube <- associate(w.all.matrix, "sube")
nb.upp <- associate(w.all.matrix, "upp")
nb.drog <- associate(w.all.matrix, "drog")

# create similarity matrices for the documents
all.docsim = cosine(w.all.matrix)
sp.docsim = cosine(w.sp.matrix)
sw.docsim = cosine(w.sw.matrix)
all.tgt.docsim = cosine(w.all.tgt.matrix)
sp.tgt.docsim = cosine(w.sp.tgt.matrix)
sw.tgt.docsim = cosine(w.sw.tgt.matrix)
# truncate rownames and colnames
# data with distractor items
rownames(sp.docsim) = substr(rownames(sp.docsim), 5, 14)
rownames(sw.docsim) = substr(rownames(sw.docsim), 5, 14)
rownames(all.docsim) = substr(rownames(all.docsim), 5, 14)
colnames(sp.docsim) = substr(colnames(sp.docsim), 5, 14)
colnames(sw.docsim) = substr(colnames(sw.docsim), 5, 14)
colnames(all.docsim) = substr(colnames(all.docsim), 5, 14)
# data without distractor items
rownames(sp.tgt.docsim) = substr(rownames(sp.tgt.docsim), 5, 14)
rownames(sw.tgt.docsim) = substr(rownames(sw.tgt.docsim), 5, 14)
rownames(all.tgt.docsim) = substr(rownames(all.tgt.docsim), 5, 14)
colnames(sp.tgt.docsim) = substr(colnames(sp.tgt.docsim), 5, 14)
colnames(sw.tgt.docsim) = substr(colnames(sw.tgt.docsim), 5, 14)
colnames(all.tgt.docsim) = substr(colnames(all.tgt.docsim), 5, 14)

# plot similarity matrices as heat maps
heatmap(sp.docsim, Rowv=NA, Colv=NA,
        main="Distance among docs -- Spanish")
heatmap(sw.docsim, Rowv=NA, Colv=NA,
        main="Distance among docs -- Swedish")
heatmap(all.docsim, Rowv=NA, Colv=NA,
        main="Distance among docs -- all")


## MDS of distances between documents, based on Sw, Sp and all data
par(mfrow=c(1,2))
# WITH distractor items
# Swedish
sw.mds <- cmdscale(1-sw.docsim, eig=TRUE, k=2)
x <- sw.mds$points[,1]
y <- sw.mds$points[,2]
plot(x, y, xlab="Coordinate 1", ylab="Coordinate 2",
     main="MDS of videoclips for Swedish data", )
text(x, y, labels = row.names(sw.docsim), cex=.7) 
# Spanish
sp.mds <- cmdscale(1-sp.docsim, eig=TRUE, k=2)
x <- sp.mds$points[,1]
y <- sp.mds$points[,2]
plot(x, y, xlab="Coordinate 1", ylab="Coordinate 2",
     main="MDS of videoclips for Spanish data", )
text(x, y, labels = row.names(sp.docsim), cex=.7)
# All
all.mds <- cmdscale(1-all.docsim, eig=TRUE, k=2)
x <- all.mds$points[,1]
y <- all.mds$points[,2]
plot(x, y, xlab="Coordinate 1", ylab="Coordinate 2",
     main="MDS of videoclips for all data", )
text(x, y, labels = row.names(all.docsim), cex=.7)

# WITHOUT distractor items
# Swedish
sw.tgt.mds <- cmdscale(1-sw.tgt.docsim, eig=TRUE, k=2)
x <- sw.tgt.mds$points[,1]
y <- sw.tgt.mds$points[,2]
plot(x, y, xlab="Coordinate 1", ylab="Coordinate 2",
     main="MDS of videoclips for Swedish data (targets only)", )
text(x, y, labels = row.names(sw.tgt.docsim), cex=.7) 
# Spanish
sp.tgt.mds <- cmdscale(1-sp.tgt.docsim, eig=TRUE, k=2)
x <- sp.tgt.mds$points[,1]
y <- sp.tgt.mds$points[,2]
plot(x, y, xlab="Coordinate 1", ylab="Coordinate 2",
     main="MDS of videoclips for Spanish data (targets only)", )
text(x, y, labels = row.names(sp.tgt.docsim), cex=.7)
# All
all.tgt.mds <- cmdscale(1-all.tgt.docsim, eig=TRUE, k=2)
x <- all.tgt.mds$points[,1]
y <- all.tgt.mds$points[,2]
plot(x, y, xlab="Coordinate 1", ylab="Coordinate 2",
     main="MDS of videoclips for all data (targets only)", )
text(x, y, labels = row.names(all.tgt.docsim), cex=.7)


## Hierarchical clustering
# Swedish data
par(mfrow=c(1,2))
d <- dist(1-sw.tgt.docsim) # euclidean distances matrix from dissimilarity matrix
fit <- hclust(d, method="ward")
plot(fit,
     main="Dendogram for Swedish data: target items",
     xlab="videoclips") # display dendogram
groups <- cutree(fit, k=7) # cut tree into 5 clusters
rect.hclust(fit, k=7, border="red") # draw dendogram with red borders around the 5 clusters
# Spanish data
d <- dist(1-sp.tgt.docsim) # euclidean distances matrix from dissimilarity matrix
fit <- hclust(d, method="ward")
plot(fit,
     main="Dendogram for Spanish data: target items",
     xlab="videoclips") # display dendogram
groups <- cutree(fit, k=7) # cut tree into 5 clusters
rect.hclust(fit, k=7, border="red")
