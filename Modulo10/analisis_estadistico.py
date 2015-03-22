
# coding: utf-8

# #Analisis Estadístico
# ### Por: Javier Serrano
# 
# El objetivo de este análisis es obtener una regresión lineal, de un cruce de divisas a partir de las series de índices y tipos asociados a ambas divisas*.
# 
# Primero importamos las librerías necesarias para realizar los análisis, vamos a utilizar principalmente 5 librerías: [numpy](http://docs.scipy.org/doc/), [pandas](http://pandas.pydata.org/pandas-docs/dev/index.html), [matplotlib](http://matplotlib.org/), [scipy](http://docs.scipy.org/doc/) y [statsmodels](http://statsmodels.sourceforge.net/devel/index.html#).
# 
# <p style="font-size:10px;">*Los datos se corresponden a series reales</p>

# In[1]:

import pandas as pd
import pickle as pkl
import itertools as itt
import statsmodels.api as sm
from scipy import stats as st 
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from pandas.tools.plotting import scatter_matrix
from statsmodels.stats.anova import anova_lm

get_ipython().magic(u'pylab inline')


# Tenemos los datos guardados en el fichero `indicators.pk`, el formato de los datos es: Close = [Open,High,Low,Close], Indices = [indice1, indice2], Tipos = [tipo1,tipo2] siendo en todo caso los indices de los dataframes, las fechas de cada valor.
# 
# Además calculamos los rendimientos diarios porcentuales de todas las series.

# In[2]:

DATA = pkl.load(open('indicators.pk','r'))
cur, ind, irs = DATA['cur'], DATA['ind'], DATA['irs']

ind_norm = pd.DataFrame(ind.pct_change()[1:],index=ind.index[1:],columns=['c1','c2'])
irs_norm = pd.DataFrame(irs.pct_change()[1:],index=irs.index[1:],columns=['c1','c2'])
close = pd.DataFrame(cur.pct_change()[1:],index=cur.index[1:],columns=['c'])

f,axs = plt.subplots(1,3,figsize=(18,4))
for data,tt,ax in zip([cur['c'], ind, irs],['Close', 'Indices', 'Tipos'],axs): data.plot(title=tt,ax=ax)


# Por otro lado vamos a ampliar las features iniciales utilizando distintas combinaciones de índices y tipos, ya que en principio, la evolución del cruce de divisas depende de la posición relativa de las series (índices|tipos) de cada divisa

# In[3]:

data = close.join(ind_norm.join(irs_norm,lsuffix='.ind',rsuffix='.irs'))
data.columns = ['c','ind1','ind2','irs1','irs2']
data['ind'] = (1+ind_norm['c1']/1+ind_norm['c2'])
data['irs'] = (1+irs_norm['c1']/1+irs_norm['c2'])
data['indB'] = (ind_norm['c1']-ind_norm['c2'])
data['irsB'] = (irs_norm['c1']-irs_norm['c2'])

f,axs = plt.subplots(1,3,figsize=(18,4))
for dt,tt,ax in zip([data['c'], data[['ind1','ind2']], data[['irs1','irs2']]],['Close', 'Indices', 'Tipos'],axs): dt.plot(title=tt,ax=ax,alpha=0.4)   


# Hagamos un primer análisis y obtengamos los momentos estadísticos de orden 1 a 4, para tener una idea de cómo se distribuyen los datos:

# In[4]:

statistics,statistics.columns = pd.concat([data.mean(),data.var(),data.skew(),data.kurt()],1),['mean','var','skew','kurt']
statistics.T


# Veamos una estimación de la distribución de la densidad utilizando un suavizado basado en kernels gaussianos:

# In[5]:

f,axs = plt.subplots(1,3,figsize=(18,4))
for dt,tt,ax in zip([data['c'], data[['ind1','ind2']], data[['irs1','irs2']]],['Close', 'Indices', 'Tipos'],axs): dt.plot(kind='kde', title=tt,ax=ax,alpha=0.4)


# ## Análisis de normalidad y homogeneidad
# 
# Como primer paso, nos planteamos si tiene sentido utilizar estas 2 familias de series, y un primer caso en el que encontramos una falta de sentido es si en ambas familias (tipo e índices) la información aportada fuera muy similar. Por este motivo el primer paso es comprobar la homogeneidad de las muestras, si tipos e índices fueran altamente homogéneos, sería dudoso el valor que se podría esperar de utilizar ambas series sería dudoso, ya que estaríamos empleando información redundante.
# 
# Por otro lado ya hemos comprobado los elevados valores de curtosis obtenidos, lo que hace que dudemos mucho de la normalidad de estas series, presunción ante la cuál muchos métodos quedarían invalidados. Por este motivo, se ha utilizado el test de Shapiro-Will para comprobar los valores de normalidad, aceptándo las distribuciones como normales si `p-value>.05` 

# In[6]:

f,axs = plt.subplots(2,2,figsize=(14,8))
for col,ax in zip(['ind1','ind2','irs1','irs2'],axs.flat):
    st.probplot(data[col][100:-100], plot=ax)
    F,p = st.shapiro(data[col][100:-100])
    ax.set_title('Probability Plot '+col.capitalize(),fontsize=10)
    ax.text(0.3, 0.7,'Shapiro:\n  W-score: {:.2f}\n  p-value: {:.2f}'.format(F,p), transform=ax.transAxes)
f.subplots_adjust(.09,.06,.97,.94,.2,.24)


# Como vemos en estas confdiciones **NO** Podemos asumir normalidad en los datos. en todos los casos el `p-value` obtenido del test de Sahpiro-Will es muy cercano a 0. Por este motivo para comprobar la homogeneidad de las distintas series, debemos utilizar otros métodos distintos al ANOVA.
# 
# Para comprobar si las poblaciones presentan la misma distribución (hipótesis nula) hemos recurrido al test de [Krusal-Wallis](http://es.wikipedia.org/wiki/Prueba_de_Kruskal-Wallis) se puede ver más información sobre el test [aquí](https://statistics.laerd.com/spss-tutorials/kruskal-wallis-h-test-using-spss-statistics.php)
# 
# Las Hipótesis son las siguientes:
#     $$H_0: Pr(Ind) = Pr(Irs)$$
#     $$H_1: Pr(Ind) \ne Pr(Irs)$$

# In[7]:

cols = ['ind1','ind2','irs1','irs2']
test = pd.DataFrame({"%s-%s"%(cols[i],cols[j]):st.kruskal(data[cols[i]],data[cols[j]]) for i,j in list(itt.combinations(xrange(4),2))}).T
test[2] = test[1]>.05
test.columns = ['F','p-value','$$H_0$$']
test


# Como se aprecia en la tabla anterior relativa a los test, las series de tipos de interés y de índices si presentan entre sí las mismas poblaciones, pero cuando comprobamos si alguna serie de índices se parece a alguna de tipos de interés, observamos que no se acepta la hipótesis nula, es decir, los tipos de interés son lo suficientemente diferentes de los índices.

# ## Análisis de correlación en el espacio ampliado
# 
# Algo que nos resulta muy interesante es saber si las variables ampliadas están muy correlacionadas con la variable objetivo o no, es de esperar que cuanto mayor correlación, mayor probabilidad de ajuste.

# In[8]:

ax = scatter_matrix(data[['c','ind','irs','indB','irsB']],diagonal='kde',figsize=(12,6))
data[['c','ind','irs','indB','irsB']].corr()


# Se observa que las nuevas features obtenidas a partir de los índices y los tipos de interés poseen una baja correlación con la divisa. Vamos por tanto a calcular un modelo de regresión lineal en función de esas nuevas variables, pero las posibilidades de éxito parece escasas a priori.
# 
# ## Modelo de regresión lineal

# In[9]:

mod = smf.ols('c ~ ind + irs + indB + irsB', data)
res = mod.fit()
print res.summary()


# En función de la tabla anterior, observamos algunos datos que nos indican que el ajuste a la nomral no es muy bueno, todos los criterios apartan bastante los valores de los esperados para una distribución normal.
# 
# A continuación imprimimos los valores estimados `res.fittedvalues` por un lado, junto con la variable a estimar original.

# In[10]:

print "\nLinearity test, F-test: {:.2f}, p-value: {:.2f}\n\n".format(*sm.stats.linear_rainbow(res))

problem = pd.concat([data['c'],res.fittedvalues],1)
problem.columns = ['real','predicted']
f,axs = plt.subplots(1,2,figsize=(16,4))
(problem['2000-01-01':'2001-01-01']+1).cumprod().plot(ax=axs[0])
(problem+1).cumprod().plot(ax=axs[1])


# En las gráficas anteriores, apreciamos que aunque localmente puede existir un buen ajuste (año 2000) es difícil que encontremos un modelo que se ajuste bien a todo el histórico. por ello se propone calcular localmente regresiones lineales para obtener mejores modelos locales.
# 
# ## Ajuste local
# 
# A continuación dividimos el intervalo para obtener 22 aproximaciones locales (de duración 261, es decir un año laborable aproximadamente) y calculamos las regresiones líneales para los mismos.

# In[11]:

from sklearn.cross_validation import KFold

NLOCAL = data.shape[0]/261 # numero de aproximaciones locales

kf = KFold(data.shape[0],NLOCAL)
all_res = [smf.ols('c ~ ind + irs + indB + irsB', data.ix[k,:]).fit() for _,k in kf]
fittedvalues = pd.concat([r.fittedvalues for r in all_res])

problem2 = pd.concat([data['c'],fittedvalues],1)
problem2.columns = ['real','predicted']
f,axs = plt.subplots(1,2,figsize=(16,4))
(problem2['2000-01-01':'2001-01-01']+1).cumprod().plot(ax=axs[0])
(problem2+1).cumprod().plot(ax=axs[1])


# En este caso apreciamos claramente que cuando ajustamos el modelo localmente, este mejora considerablemente. 
# 
# Para comprobar como un ajuste local mejora, vamos a dividir de nuevo el problema en frecuencia mensual (21 datos o aproximadamente 100 modelos).

# In[12]:

NLOCAL2 = data.shape[0]/21 # numero de aproximaciones locales

kf2 = KFold(data.shape[0],NLOCAL2)
all_res2 = [smf.ols('c ~ ind + irs + indB + irsB', data.ix[k,:]).fit() for _,k in kf2]
fittedvalues2 = pd.concat([r.fittedvalues for r in all_res2])

problem3 = pd.concat([data['c'],fittedvalues2],1)
problem3.columns = ['real','predicted']
f,axs = plt.subplots(1,2,figsize=(16,4))
(problem3['2000-01-01':'2001-01-01']+1).cumprod().plot(ax=axs[0])
(problem3+1).cumprod().plot(ax=axs[1])


# ### Error en ajustes locales
# 
# Vamos a tomar una medida del error de cada aproximación local en el intervalo siguiente:
# 

# In[13]:

from statsmodels.tools.eval_measures import mse

ixs = list(kf2)
p = all_res2[1]
ypred = p.predict(data.ix[ixs[2][1],['ind','irs','indB','irsB']])
ynext = pd.DataFrame(np.c_[data.ix[ixs[2][1],'c'],ypred])
ynext.columns = ['real','prediction']
ynext.plot()

print "in range: {}, out of range: {}".format(p.mse_model,mse(data.ix[ixs[2][1],'c'],ypred))


# Se observa un incremento en el `MSE` de un 100%, al intentar predecir las variables en erl siguiente intervalo, utilizando los parámetros dados del intervalo anterior

# ## Pasos siguientes.
# 
# A continuación indicamos una serie de pasos que se podrían llevar a cabo para un análisis en profundidad:
# 
# Sobre el estudio de los modelos locales:
# 
# - Análisis local de todos los residuos
# - Comprobación local de normalidad
# - Estudio local de correlación
# - medir el error fuera del intervalo de optimización del modelo
# 
# Sobre el estudio de nuevas variables:
# 
# - Intentar aproximaciones sobre otras variables (por ejemplo una regresión logística sobre el signo del rendimiento)
# - Ampliar el espacio de features local
# 
# Además, también podemos utilizar el paquete [sklearns](http://scikit-learn.org/stable/) para construir regresiones y probar mejor el ajuste a nuevos DATOS.
# 
