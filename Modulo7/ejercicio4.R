
if (!(require("MicroDatosEs", character.only=T, quietly=T))) {
  install.packages("MicroDatosEs")
  library("MicroDatosEs", character.only=T)
}
if (!(require("data.table", character.only=T, quietly=T))) {
  install.packages("data.table")
  library("data.table", character.only=T)
}
if (!(require("plyr", character.only=T, quietly=T))) {
  install.packages("plyr")
  library("plyr", character.only=T)
}
if (!(require("dplyr", character.only=T, quietly=T))) {
  install.packages("dplyr")
  library("dplyr", character.only=T)
}
if (!(require("reshape2", character.only=T, quietly=T))) {
  install.packages("reshape2")
  library("reshape2", character.only=T)
}

PATH <- "~/Documentos"
FILENAME <- "MicrodatosCP_NV_per_bloque1.txt"
FULLPATH <- paste(PATH,FILENAME,sep="/")

features <- c("cpro", "factor", "edad", "sexo", "escolar", "esreal", "nhijos", "internet")

df <- censo2010(FULLPATH)
df <- as.data.frame(df[,features])
df <- head(df,n=100000)

bins <- c(1,5,10,15,18)

dplyr.df = TRUE
dt.df = TRUE

##################################################################################################
#                   tabulacion por menores de edad con internet usando dplyr 
##################################################################################################
if (dplyr.df==TRUE){
  dplyr.df.target <-  df %>%
    filter(edad<18) %>%
    mutate(edad_bin = cut2(edad,bins))
  
  dplyr.df.result <- dplyr.df.target %>%
    group_by(internet, edad_bin) %>%
    mutate(number=length(internet)) %>%
    ungroup() %>%
    group_by(internet,edad,edad_bin,number) %>%
    summarize()
  
  dplyr.df.tabla <- dcast(dplyr.df.result, internet ~ edad_bin, fun.aggregate = unique, value.var="number", fill=0)
  
  #rm(list = ls(pattern="dplyr.df.")) 
}

##################################################################################################
#                 tabulacion por menores de edad con internet usando data.table 
##################################################################################################

if (dt.df==TRUE){
  dt.df.base <- as.data.table(df)
  
  dt.df.target <- dt.df.base[edad<18,][,edad_bin := cut2(edad,bins)]
  
  dt.df.result <- dt.df.target[,number := length(edad),by=c("internet","edad_bin")]  
  
  dt.df.tabla <- dcast(dt.df.result, internet ~ edad_bin, fun.aggregate = unique, value.var="number", fill=0)
}