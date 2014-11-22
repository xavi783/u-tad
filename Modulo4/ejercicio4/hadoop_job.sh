# binarios de hadoop
export HADOOP_HOME="/usr/local/hadoop/bin"
export PATH="$HADOOP_HOME:$PATH"

# servicios hadoop
export HADOOP_STRM="/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.4.0.jar"

# alias para ejecutar los ejercicios
alias test_local = 'head ../facturas.txt | ./mapper.py | sort -k1 | ./reducer.py'
alias test_hadoop="hadoop jar $HADOOP_STRM -files '../toolbox' -input '../facturas.txt' -output 'results' -mapper 'mapper.py' -reducer 'reducer.py' -file '../clientes.txt'"