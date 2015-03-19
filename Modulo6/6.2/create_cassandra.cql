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
 --		     cqlsh> SOURCE 'create_cassandra.cql';

CREATE KEYSPACE IF NOT EXISTS stocks WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1 };

USE stocks;

-- Elimina la tabla 'nyse' si existe (asi aseguramos subir solo los datos que queremos)
DROP TABLE IF EXISTS nyse;

-- Crea un modelo de datos (si no existe la tabla 'nyse'), con formato:
--		{symbol text, fecha timestamp, return double}
-- Utiliza symbol como CLUSTERING KEY para almacenar consecutivamente en disco por empresa
-- y fecha como parte de la PRIMARY KEY
CREATE TABLE IF NOT EXISTS nyse
(symbol text,
 fecha timestamp,
 return double,
 PRIMARY KEY ((symbol), fecha)
);