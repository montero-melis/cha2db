library('lsa')

# create text matrix from Documents;
# each doc is the added descriptions for each videoclip of all participants
sp.matrix <- textmatrix("C:\\Documents and Settings\\gumo8029\\Mina dokument\\hopi_docs_lsa_input\\docs_spa")
sw.matrix <- textmatrix("C:\\Documents and Settings\\gumo8029\\Mina dokument\\hopi_docs_lsa_input\\docs_swe")
all.matrix <- textmatrix("C:\\Documents and Settings\\gumo8029\\Mina dokument\\hopi_docs_lsa_input\\docs_all")

# Apply weighting schemes for each of the matrices above
# local weighting: log(type freq +1); global weighting: entropy
w.sp.matrix <- lw_logtf(sp.matrix)*gw_entropy(sp.matrix)
w.sw.matrix <- lw_logtf(sw.matrix)*gw_entropy(sw.matrix)
w.all.matrix <- lw_logtf(all.matrix)*gw_entropy(all.matrix)

# examples of related terms
associate(w.all.matrix, "sube")
associate(w.all.matrix, "upp")
associate(w.all.matrix, "drog")

# create similarity matrices for the documents
all.docsim = cosine(w.all.matrix)
sp.docsim = cosine(w.sp.matrix)
sw.docsim = cosine(w.sw.matrix)

# plot similarity matrices as heat maps
heatmap(sp.docsim, Rowv=NA, Colv=NA,
        main="Distance among docs -- Spanish")
heatmap(sw.docsim, Rowv=NA, Colv=NA,
        main="Distance among docs -- Swedish")
heatmap(all.docsim, Rowv=NA, Colv=NA,
        main="Distance among docs -- all")

# Which documents are highly correlated
sp.docsim[which(sp.docsim > 0.8 & sp.docsim < 1)]
# TODO: extract the dimension names for all these values
# i.e. which pairs of documents are highly correlated
# Different approach: create new matrix keeping only rows/columns
# that have at least one high correlation
sp.docsim2 <- sp.docsim
diag(sp.docsim2) <- rep(0, length(diag(sp.docsim2)))
apply(sp.docsim2, 1, max)

