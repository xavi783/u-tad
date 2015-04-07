
# Memoria
### Por: Javier Serrano

El Objetivo del presente trabajo es describir el método de trabajo para predecir la probabilidad de impago de un cliente.

## Feature Engineering

El primer paso es estudiar la información, intentar establecer relaciones entre las variables e incluso modificar las dimensiones del espacio de variables, utilizando combinaciones de las mismas o variables derivadas.

Existen muchas formas de descubrir esas relaciones, pero principalmente podemos dividirlas en 2 líneas

* Con conocimiento del dominio: se trata de estudiar los conceptos que representan las variables (en caso de que estos sean conocidos), aplicar el conocimiento (o el sentido común) para establecer, a priori, posibles relaciones que se pueden dar entre las variables y a continuación diseñar pruebas para intentar confirmar dichas relaciones. En caso de confirmarse estas relaciones, se pueden combinar las variables de entradas según estas mismas para crear una nueva variable (feature) en el problema.
* Sin conocimiento del dominio: Se trata de probar modelos o técnicas de data science para buscar relaciones en el problema sin tener en cuenta el significado de dichas relaciones o porqué se producen.

Ambos enfoques no son excluyentes, de hecho lo recomendable sería aplicar ambos para un buen estudio del problema.

### FE con conocimiento del dominio.

Empecemos por considerar la primera vía, en este caso se puede aplicar ya que conocemos los conceptos que representan las variables de entrada.

En este caso vemos varios grupos distintos de variables:

* Estructura de los "days past due":
	* NumberOfTime30-59DaysPastDueNotWorse 	
	* NumberOfTime60-89DaysPastDueNotWorse
	* NumberOfTimes90DaysLate
* Numero de deudas abierto:
	* NumberOfOpenCreditLinesAndLoans
	* NumberRealEstateLoansOrLines
* Datos de estructura familiar:
	* age
	* MonthlyIncome
	* NumberOfDependents
	* DebtRatio (dudosa la clasificación en este grupo)
* Otros:
	* SeriousDlqin2yrs
	* RevolvingUtilizationOfUnsecuredLines
