-- 
 -- Para ejecutar este script:
 --		1. Ir a la carpeta donde se encuentra este script (usando el Gestor de Archivos 
 --		   PCManFM) y abrir una terminal (pulsar F4)
 --		2. asegurarse de tener corriendo el servidor de Cassandra-2.1.2, para eso tras añadir
 --		   al PATH la carpeta 'bin' de cassandra, escribir:
 --			 $ cassandra
 --		   esto deberia ejecutar automaticamente el servidor de cassandra
 --		3. a continuacion, ejecutar una nueva terminal, para eso, desde la propia terminal
 --		   ejecutar ctr+shift+T, en esa terminal (debe estar en la carpeta donde tenemos los
 --		   script) ejecutar:
 --			 $ cqlsh
 --		   esto abrira la tyerminal de cql
 --		4. Ejecutar el script mediante la sentencia:
 --		     cqlsh> SOURCE 'import_cassandra.cql';

USE stocks;

-- Cargamos los datos del archivo 'nyse_result.csv/part-r-00000'
-- Por algun motivo no he podido crear un archivo csv directamente aunque el part-r-00000
-- tiene formato csv
COPY nyse (symbol, fecha, return) FROM 'nyse_result.csv/part-r-00000';