if (!(require("rgdal", character.only=T, quietly=T))) {
  install.packages("rgdal")
  library("rgdal", character.only=T)
}
if (!(require("pxR", character.only=T, quietly=T))) {
  install.packages("pxR")
  library("pxR", character.only=T)
}
if (!(require("dplyr", character.only=T, quietly=T))) {
  install.packages("dplyr")
  library("dplyr", character.only=T)
}

YEAR <- 1989
PATH <- "/home/x/Documentos/cursos/UTAD/u-tad-modulo7_1/ccaa"

layer <- "recintos_autonomicas_inspire_peninbal_etrs89"
if (Sys.info()['sysname']=="Linux"){
  dsn <- paste(PATH,"/recintos_autonomicas_inspire_peninbal_etrs89",sep="")
}
if (Sys.info()['sysname']=="Windows"){
  dsn <- PATH  
}
maps <- readOGR(dsn,layer,encoding="latin1")
maps.data <- maps@data

# estadisticas del IRPF: http://www.ine.es/jaxi/menu.do?type=pcaxis&path=/t45/p062/a04/&file=pcaxis
values <- c('http://www.ine.es/pcaxisdl//t45/p062/a04/l0/ir40001.px',
            'http://www.ine.es/pcaxisdl//t45/p062/a04/l0/ir40002.px',
            'http://www.ine.es/pcaxisdl//t45/p062/a04/l0/ir40003.px')
concepts <- c('IRPF_concepto_periodo','IRPF_tipo_concepto_periodo','IRPF_ccaa')
filenames <- data.frame(concepts,values)

data <- read.px(filename=as.character(filenames[3,2]),encoding="latin1")
info.data <- data$DATA$value[data$DATA$value$periodo==YEAR & data$DATA$value$tipo=='TOTAL (1)',]

ccaa.getid <- function(comunidades){
  ccaa.re <- c('Andaluc.a', 'Arag.n', 'Asturias', 'Balear.+', 'Canarias', 'Cantabria', 'Castilla.*Le.n',
               'Castilla.*Mancha', 'Catalu.a', 'Valencia.', 'Extremadura', 'Galicia', 'Madrid',
               'Murcia', 'Navarra', 'Pa.s.Vasco', 'Rioja', 'Ceuta', 'Melilla')
  unlist(lapply(comunidades,
         function(comunidad){
            result <- c(1:length(ccaa.re))[unlist(
                      lapply(ccaa.re,
                        function(x) grepl(x, as.character(comunidad), perl=TRUE))
                      )]
            if(length(result)==0){
             return(NA)
            }else{
             return(result)
            }
          }))
}

info.data <- info.data %>%
              mutate(ccaa.id=ccaa.getid(info.data$CCAA))
maps.data <- maps.data %>%         
              mutate(ccaa.id=ccaa.getid(maps.data$NAMEUNIT))
maps@data <- join(maps.data, info.data, by=c("ccaa.id" = "ccaa.id"))

colores <- rainbow(length(maps@plotOrder),start=0, end=4/6)
title <- list(label=paste("IRPF por CCAA",as.character(YEAR),sep=" - "),cex=1)
plotMap <- spplot(maps, zcol="value",col.regions=colores[seq(length(colores),1,-1)], main=title)
plotMap
