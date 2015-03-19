-- run preparar_modelo.pig
 -- PREPARAR_MODELO script para tratar el fichero 'NYSE_daily.tsv' y generar el modelo de datos
 -- enriquecido con con formato: [symbol, fecha, return = (Open - Close)/avg_month(Open-Close)]
 -- que se exportara como CSV
 --
 -- Para ejecutar este script:
 --		1. Ir a la carpeta donde se encuentra este script (usando el Gestor de Archivos 
 --		   PCManFM) y abrir una terminal (pulsar F4)
 --		2. si no esta en el archivo ~/.bashrc ejecutar la sentencia:
 --			$ export PATH = "<path/to/pig>/bin:$PATH"
 --		   sustituyendo <path/to/pig> por la ruta a la carpeta con la distibucion pig
 --		3. ejecutar en la terminal:
 --			$ pig -x local
 --		   con esto tendremos pig corriendo en modo local y tendremos acceso a los
 --		   archivos que habia en la carpeta donde se ejecuto la terminal
 --		4. ejecutar en la consola de pig:
 --			grunt> run preparar_modelo.pig

-- Cargar los datos planos del fichero 'NYSE_daily.tsv', ver la sentencia
-- para mas detalles sobre el formato
nyse = LOAD 'NYSE_daily.tsv'
USING PigStorage('\t')
AS (exchange:chararray,
	symbol:chararray,
	fecha:datetime,
	open:double,
	high:double,
	low:double,
	close:double,
	volume:long,
	adj_close:double);
nyse = ORDER nyse BY symbol, fecha;

-- extraer los años y meses de las fechas y calcula la diferencia open - close.
 -- FORMATO:
 --		[symbol, fecha, year, month, return=(open-close)]
 -- NOTA: ordena los archivos por (symbol, year, month) que actua como PRIMARY KEY
nyse_months = FOREACH nyse 
GENERATE symbol AS symbol,
		 ToString(fecha,'yyyy-MM-dd') AS fecha,
		 GetYear(fecha) AS year,
		 GetMonth(fecha) AS month,
		 (open-close) AS return;
nyse_months = ORDER nyse_months BY symbol, year, month;	

-- agrupa por symbol, año y mes y genera un modelo enriquecido con
 -- FORMATO
 --		[symbol, year, month, media]
 -- NOTA: toma solo los registros distintos, hago esto porque de la 
 -- sentencia anterior se generan multiples registros iguales, se 
 -- estima que un registro por cada uno de `nyse_months`
nyse_monthly_returns = FOREACH (
	GROUP nyse_months
	BY (symbol, year, month))
GENERATE FLATTEN(nyse_months.symbol) AS symbol,
		 FLATTEN(nyse_months.year) AS year,
		 FLATTEN(nyse_months.month) AS month,
		 AVG(nyse_months.return) AS media;
nyse_monthly_returns = DISTINCT nyse_monthly_returns;

-- unimos nyse_months y nyse_monthly_returns por (symbol, año y mes)
nyse_monthly =JOIN nyse_months BY (symbol, year, month), nyse_monthly_returns BY (symbol, year, month);

-- eliminamos las columnas no necesarias y calculamos la division, para obetner:
-- FORMATO:
--		[symbol, fecha, return = Open-Close/avg_month(Open-Close)]
result = FOREACH nyse_monthly 
GENERATE nyse_months::symbol AS symbol,
		 nyse_months::fecha AS fecha,
		 nyse_months::return/nyse_monthly_returns::media AS return;

-- guardamos los datos en el archivo* 'nyse_result.csv'
STORE result INTO 'nyse_result.csv' USING PigStorage(',');