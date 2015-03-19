u-tad
=====

Este es el repositorio con los ejercicios del máster primera edición de Data Science U-TAD.

## Modulo 4
 Este modulo contiene 5 ejercicios de hadoop mas un toolbox de readers, mapper y reducers simples para resolver los ejercicios asi como los codigos de map/reduce propios de cada ejercicio.

 En cada carpeta ademas se adjunta un script de linux que permite ejecutar los trabajos de 2 formas diferentes:

 * Por un lado se pueden lanzar en local, para ello se debe ejecutar `. command.sh` y despues `test_local`
 * Por otro lado se pueden lanzar contra hadoop, primero ejecutando `. command.sh` y despues `test_hadoop`

 Tambien se adjunta una carpeta `/results` con los resultados obtenidos de la ejecucion contra hadoop, asi como los archivos txt con los datos necesarios para hacer las pruebas

## Directorios

```
   UTAD
    ├── LICENSE
    ├── Modulo4
    │   ├── clientes.txt
    │   ├── ejercicio1
    │   │   ├── command.sh
    │   │   ├── mapper.py
    │   │   ├── reducer.py
    │   │   └── results
    │   │       ├── part-00000
    │   │       └── _SUCCESS
    │   ├── ejercicio2
    │   │   ├── command.sh
    │   │   ├── mapper.py
    │   │   ├── reducer.py
    │   │   └── results
    │   │       ├── part-00000
    │   │       └── _SUCCESS
    │   ├── ejercicio3
    │   │   ├── command.sh
    │   │   ├── mapper.py
    │   │   ├── reducer.py
    │   │   └── results
    │   │       ├── part-00000
    │   │       └── _SUCCESS
    │   ├── ejercicio4
    │   │   ├── command.sh
    │   │   ├── mapper.py
    │   │   ├── reducer.py
    │   │   └── results
    │   │       ├── part-00000
    │   │       └── _SUCCESS
    │   ├── facturas.txt
    │   └── toolbox
    │       ├── hmappers
    │       │   ├── __init__.py
    │       │   ├── simple_mapper.py
    │       ├── hreaders
    │       │   ├── __init__.py
    │       │   ├── token_readers.py
    │       ├── hreducers
    │       │   ├── __init__.py
    │       └── └── list_reducer.py
    └── README.md

```