library(focus)
library(Rtsne)
library(RColorBrewer)

#data = read.csv("data.csv")
X = c()
groups = c()
labels = c()
depth1 = c()
depth2 = c()
gid = 1
for( i in seq(128, 229, 17) ){
   tmp = data[,i:(i+16)]
   colnames(tmp) <- 1:17;
   X = rbind(X, tmp )
   groups = c(groups, rep(gid, nrow(data) ) )
   gid = gid+1
   labels = c(labels, data$label)
   depth1 = c(depth1, rep(1:256, 127) )
   depth2 = c(depth2, rep(1:127, 256) )
}
labels = as.factor(labels)
groups = as.factor(groups)

res = focus.setup.6way(X, labels) #groups)

Xdup = duplicated(X)
Xtsne = Rtsne(X[!Xdup, ])

pal = brewer.pal("Set1", n=9)

plot(Xtsne$Y, col=pal[groups[!Xdup]], pch=".")
