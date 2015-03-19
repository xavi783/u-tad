u-tad-modulo7_1
===============

[Página web del proyecto](http://xavi783.github.io/u-tad-modulo7_1)


* [Clases S4 y mapas (2 puntos)](http://xavi783.github.io/u-tad-modulo7_1/ejercicio1.html)
* [JSON & XML (2 puntos)](http://xavi783.github.io/u-tad-modulo7_1/ejercicio2.html)
* [Web scraping, texto y fechas (2 puntos)](http://xavi783.github.io/u-tad-modulo7_1/ejercicio3.html)
* [plyr, dplyr y data.table (2 puntos)](http://xavi783.github.io/u-tad-modulo7_1/ejercicio4.html)
* [RHadoop (2 puntos)](http://xavi783.github.io/u-tad-modulo7_1/ejercicio5.html), Para instalar RHadoop en linux:

	**Descargar RHadoop**
	
		https://github.com/RevolutionAnalytics/RHadoop/wiki

	**Instalar rJava**
	1. Editar /usr/lib/R/etc/javaconf
	2. Añadir path: ${JAVA_HOME="/usr/local/java/jdk1.7.0_71"}
	3. Ejecutar: $ sudo R CMD javareconf

	**Configurar R**
	
	1. Ejecutar:
	
		Sys.setenv("HADOOP_PREFIX"="/usr/local/hadoop-2.6.0")
		
		Sys.setenv("HADOOP_CMD"="/usr/local/hadoop-2.6.0/bin/hadoop")
		
		Sys.setenv("HADOOP_STREAMING"="/usr/local/hadoop-2.6.0/contrib/streaming/hadoop-streaming-1.1.2.jar")

	**Basado en :**

		http://www.rdatamining.com/big-data/r-hadoop-setup-guide
	
* [Ejercicio extra (2 puntos):](https://github.com/xavi783/u-tad-modulo7_1/blob/master/jserrano_1.0.tar.gz)
	
	1. En Linux: descargar el paquete en formato *.tar.gz, para eso ejecutar en la terminal
	
			$ wget https://github.com/xavi783/u-tad-modulo7_1/blob/master/jserrano_1.0.tar.gz

	2. Descomprimir el paquete con la siguiente instrucción:
	
			$ tar -xzf jserrano_1.0.tar.gz

	3. Ejecutar en RStudio e Instalar paquete devtools
	4. Instalar el paquete con las siguientes instrucciones:
	
			install(as.package("\<path/to/parent_carpeta_jserrano\>/jserrano"))
