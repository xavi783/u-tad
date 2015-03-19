
if (!(require("rjson", character.only=T, quietly=T))) {
  install.packages("rjson")
  library("rjson", character.only=T)
}
if (!(require("dplyr", character.only=T, quietly=T))) {
  install.packages("dplyr")
  library("dplyr", character.only=T)
}
if (!(require("lubridate", character.only=T, quietly=T))) {
  install.packages("lubridate")
  library("lubridate", character.only=T)
}

json2frame <- function(x.json){
  data.raw <- unlist(x.json$data)
  ncols  <- length(x.json$column_names)
  series <- lapply(c(1:ncols), function(x) seq(x,length(data.raw),ncols))
  
  x.json$data <- c()
  x.json$data <- lapply(c(1:ncols), function(x) cbind(x.json$data, data.raw[series[[x]]]))
  x.json$data <-  as.data.frame(x.json$data)
  colnames(x.json$data) <- x.json$column_names
  x.json
}

cpi.json <- fromJSON(readLines("http://www.quandl.com/api/v1/datasets/ODA/ESP_PCPIE.json"))
cpi.json <- json2frame(cpi.json)
head(cpi.json$data,n=10)

ibex35.json <- fromJSON(readLines("http://www.quandl.com/api/v1/datasets/YAHOO/INDEX_IBEX.json"))
ibex35.json <- json2frame(ibex35.json)
head(ibex35.json$data,n=10)

ibex35.json$data <- ibex35.json$data %>%
  mutate(year=year(Date))
cpi.json$data <- cpi.json$data %>%
  mutate(year=year(Date)) %>%
  mutate(Value = unlist(lapply(lapply(Value, as.character),as.numeric))) %>%
  mutate(Value_diff = c(0, diff(c(0,diff(Value)))))

combination <- left_join(ibex35.json$data, cpi.json$data, by=c("year" = "year"))
combination <- combination[!colnames(combination) %in% c("Date.y")]
colnames(combination)[2] <- "Date"
head(combination)

tabla <- combination %>%
          group_by(year) %>%
          mutate(close_ini = - unlist(lapply(lapply(Close, as.character),as.numeric)[length(Close)]) +
                   unlist(lapply(lapply(Close, as.character),as.numeric)[1])) %>%
          select(year,Value_diff,close_ini,Date) %>% top_n(n=1) %>%
          ungroup() %>% select(Date,Value_diff,close_ini)
tabla<- as.data.frame(tabla)

#Solucion
sprintf("%.2f%%",sum(sign(tabla$Value_diff)==sign(tabla$close_ini))/nrow(tabla)*100)


