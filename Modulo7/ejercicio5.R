library(rmr2)
library(data.table)

Sys.setenv("HADOOP_PREFIX"="/usr/local/hadoop-2.6.0")
Sys.setenv("HADOOP_CMD"="/usr/local/hadoop-2.6.0/bin/hadoop")
Sys.setenv("HADOOP_STREAMING"="/usr/local/hadoop-2.6.0/share/hadoop/tools/lib/hadoop-streaming-2.6.0.jar")

fnam <- "/user/x/data/datos_censo2011.tsv"           # file name
fif  <- make.input.format("csv", sep = "\t")     # file format

my.map <- function(k,v){
  bins <- c(1,5,10,15,18)
  k2 <-  which(cut(v$V8, bins)==levels(cut(v$V8, bins)))
  keyval(paste(v$V64, k2, sep=""), list(v$V64, cut(v$V8, bins)))
}

my.reduce <- function(k,v){ 
  tmp <- as.data.table(do.call(rbind, v))
  tmp <- setnames(tmp,names(tmp),c("internet","edad_bin"))
  keyval(k, list(tmp$internet[1], tmp$edad_bin[1], dim(tmp)[1])) #:=number
}

res <- from.dfs(mapreduce(
  input = fnam,
  input.format = fif,
  map = my.map
  reduce = my.reduce ))

df <- data.frame(res$val, colnames=c("internet","edad_bin"))

df.tabla <- dcast(df, internet ~ edad_bin, fun.aggregate = unique, value.var="number", fill=0)

