
# Filtrado colaborativo: películas relacionadas
recomienda.peliculas <- function(titulo, k){
  options(warn=-1)
  library(TSdist)  
  # Se cargan los datos de las peliculas
  pelis <- read.table(file="dat/ml-100k/u.item", sep ="|", quote = "")
  colnames(pelis) <- c("movie.id", "movie.title", "release.date", "video.release.date","IMDb.URL","unknown",
                       "Action", "Adventure","Animation","Children","Comedy", "Crime", "Documentary","Drama",
                       "Fantasy", "Film-Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller",
                       "War", "Western")  
  
  # Tomamos la pelicula seleccionada.
  movie.sel<-pelis[pelis$movie.title==titulo,1]
  
  # Calcula la distancia con cada palicula en función del género.
  result <-matrix(, nrow = nrow(pelis), ncol = 1)
  for(i in 1:nrow(pelis)) {
    result[i] = tsDistances(as.numeric(pelis[movie.sel,c(7:24)]), as.numeric(pelis[i,c(7:24)]), distance="euclidean")
  }
  
  # Se ordenan y nos quedamos con las k más cercanas.
  recomendaciones <- pelis[order(result)[c(2:(k+1))],]
  return (as.character(recomendaciones$movie.title))
}

# Probamos por ejemplo con Toy Story:
recomienda.peliculas('Toy Story (1995)',3)

# Filtrado Colaborativo: recomendaciones para ti
twinSouls <- function(userId, nfilms, nsouls, filmspath="dat/ml-100k/u.data"){
  options(warn=-1)
  
  # Cargamos peliculas y extraemos el usuario del que se desean calcular las almas gemelas:
  library(plyr)
  pelis <- read.table(filmspath, sep = "\t")[,1:3]
  colnames(pelis) <- c("user", "item", "rating")
  me <- pelis[pelis$user==userId,]
  
  # Calculamos la coincidencia de peliculas de cada usuario con el usuario objetivo
  coincidences <- NULL
  soul <- NULL
  for (i in 1:(length(unique(pelis$user))-1)){
    coincidences[i] <- sum(as.numeric(is.element(me$item,pelis[pelis$user==i,2])))
    soul[i] <- i
  }
  souls.all <- data.frame(soul,coincidences)[coincidences >= nfilms,]
  
  # Calculamos la correlacion de cada usuario con el usuario objetivo y nos quedamos con los NSOULS
  # que cumplen el NFILMS como limite de peliculas y mas alta correlacion tienen.
  tmp.0 <- pelis[pelis$user == me$user[1],]
  tmp.1 <- pelis[pelis$user != me$user[1],]  
  tmp <- merge(tmp.0, tmp.1, by = "item")  
  res <- ddply(tmp, .(user.y), summarize, n = length(item), cosine.dist = cor(rating.x, rating.y))
  res <- res[order(-abs(res$cosine.dist)),]  
  aux<-(res[is.element(res$user.y,souls.all$soul)==TRUE,])  
  if (nsouls==0){
    return (aux$user.y)
  }else{
    return (aux$user.y[c(1:nsouls)])
  }
}  

# En este caso y para que sea valido para cualquier fichero, se ha empleado una pequeña técnica, que
# es construir una funcion genérica para de un archivo dado, aplicarselo a un usuario y sacar sus
# almas gemelas. De esta forma es válido para cualquier usuario, si se desea un nuevousuario basta
# con ampliar el archivo, imaginemos que somos el usuario numero 100 del archivo (userId=84):
Iam <- unique(read.table("dat/ml-100k/u.data", sep = "\t")[,1])[100]

#Las almas gemelas del usuario 84, son:
twinSouls(Iam, 10, 10)

# Recomendaciones viejunas
recomendacionesViejunas <- function(age, sex, ocupation, nfilms=10){
  
  # Se cargan los datos
  users <- read.table(file="dat/ml-100k/u.user", sep ="|", quote = "") #usuarios
  pelis <- read.table("dat/ml-100k/u.data", sep = "\t")
  items <- read.table(file="dat/ml-100k/u.item", sep ="|", quote = "")
  
  # Te quedas con los usuarios de la misma edad, sexo y ocupacion.
  targetUsers <-users[is.element(users$V2,age),]
  targetUsers <-targetUsers[is.element(targetUsers$V3,sex),]
  if (dim(table(is.element(targetUsers$V4,ocupation)))>1){
    targetUsers<-targetUsers[is.element(targetUsers$V4,ocupation),]
  }  
  
  # Nos quedamos con las películas afines:
  similarUsers <- pelis[is.element(pelis$V1,targetUsers$V1),]  
  # Te quedas con las pelis mejor ranqueadas.
  bestFilms < -max(similarUsers$V3)
  recomendation <- similarUsers[is.element(similarUsers$V3,bestFilms),]
  recomendation <- item[is.element(item$V1,recomendation$V2),]
  
  # Recomiendas las pelis.
  return (head(recomendation$V2,nfilms))  
}

# Probamos una recomendacion con características similares a las mias:
recomendacionesViejunas(28, 'M', 'entertainment')

# Filtrado Colaborativo: recomendaciones
estimateRate <- function(fileNumber){
  options(warn=-1)
  
  # fileNumber: numero de la fila a predecir
  library(reshape2)
  library(softImpute)
  
  # Cargamos todas las peliculas
  pelis <- read.table("dat/ml-100k/u.data", sep = "\t")
  pelis.info <- read.table(file="dat/ml-100k/u.item", sep ="|", quote = "")[,1:3]
  colnames(pelis) <- c("user", "item", "rating")
  
  # Eliminamos la fila seleccionada.
  deleted <- pelis$rating[fileNumber]
  pelis$rating[fileNumber]<-NA  
  
  # Calculamos la media de los rating de las almas gemelas un redondeamos.
  nfilms = min(dim(pelis[pelis$user==pelis$user[fileNumber],])[1],10)
  souls <- twinSouls(pelis$user[fileNumber], nfilms, 0)
  media <- mean(pelis$rating[is.element(pelis$item[is.element(pelis$user,souls)],pelis$item[fileNumber])])
  solution.1 <- round(media, digits=0)
  
  # Calculamos las peliculas de las almas gemelas.
  aux.1 <- pelis[is.element(pelis$user,souls),]
  aux.2 <- which(pelis$user==pelis$user[fileNumber])
  souls.films <- rbind(aux.1[is.element(aux.1$item,pelis$item[aux.2]),],pelis[aux.2,])
  
  # utilizamos softImpute para realizar la imputacion, teniendo en cuenta el resto de valores.
  reshaped <- acast(souls.films, user~item, value.var="rating")
  imputation <- complete(reshaped,softImpute(reshaped,rank=15,lambda=30))
  solution.2 <- imputation[as.character(pelis$user[fileNumber]),as.character(pelis$item[fileNumber])]
  solution.2 <- round(solution.2, digits=0)
  
  return (data.frame(real=deleted, imputation.1=solution.1, imputation.2=solution.2))
}

# Probamos la funcion para la puntuacion 100 y la 100000
# Para el caso de la fila 100 vemos que las imputaciones son correctas:
estimateRate(100)
# Sin embargo para la ultima fila ambas imputaciones se desvian en 1
estimateRate(100000)