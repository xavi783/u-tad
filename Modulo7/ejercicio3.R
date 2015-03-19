
if (!(require("data.table", character.only=T, quietly=T))) {
  install.packages("data.table")
  library("data.table", character.only=T)
}
if (!(require("XML", character.only=T, quietly=T))) {
  install.packages("XML")
  library("XML", character.only=T)
}
if (!(require("stringr", character.only=T, quietly=T))) {
  install.packages("stringr")
  library("stringr", character.only=T)
}

tabla <- readHTMLTable("http://www.invertia.com/mercados/bolsa/indices/ibex-35/acciones-ib011ibex35/1a",header=TRUE,encoding="latin1")[[2]]
colnames(tabla) <- c('TKR','Last','Dif','Dif%','_','Max','Min','Volume','Capital','Rt/Div','PER','Hour')
tabla <- tabla[colnames(tabla)!="_"]

conv <- c( function(x) as.numeric(str_replace_all(x,",",".")),
           function(x) as.numeric(str_replace_all(x,"\\.","")),
           function(x) as.numeric(str_replace_all(str_replace_all(x,"%",""),",",".")),
           function(x) {      
             as.Fecha <- function(x){x = as.POSIXlt(x,format="%Y-%m-%d")}
             as.Hora <- function(x){x = as.POSIXct(x,format="%H:%M")}              
             if (any(grepl("\\d{1,2}:\\d{1,2}",x,perl=TRUE))) {
               as.Fecha(x[grepl("\\d{1,2}/\\d{1,2}/\\d{4}",x,perl=TRUE)])
             }
             if (any(grepl("\\d{1,2}:\\d{1,2}",x,perl=TRUE))) {
               as.Hora(x[grepl("\\d{1,2}/\\d{1,2}/\\d{4}",x,perl=TRUE)])
             }
             x
           })
cols<-c()
cols$numeric <- c("Last","Dif","Dif%","Max","Min","Capital","PER")
cols$millions<-c("Volume")
cols$percent <- c("Rt/Div")
cols$hour <- c("Hour")

for(i in c(1:length(names(cols)))){
  for(x in cols[[i]]){
    tabla[x]<-lapply(tabla[x],conv[[i]])[[1]]
  }
}