#!/bin/sh
# przykladowe wywolanie ./tests.sh 30
if [ "$1" != "" ]; then
    echo 'Liczba powtorzen algorytmu: ' $1
    python main.py -r 20 -t 4 -f 300 -cf 0.999 -b 0 --repeat $1
    #python main.py -r 20 -t 3 -f 300 -cf 0.999 -b 0 --repeat $1
    #python main.py -r 20 -t 2 -f 300 -cf 0.999 -b 0 --repeat $1
    #python main.py -r 20 -t 1 -f 300 -cf 0.999 -b 0 --repeat $1
    #python main.py -r 25 -t 4 -f 300 -cf 0.999 -b 0 --repeat $1
    #python main.py -r 25 -t 3 -f 300 -cf 0.999 -b 0 --repeat $1
    #python main.py -r 25 -t 2 -f 300 -cf 0.999 -b 0 --repeat $1
    #python main.py -r 25 -t 1 -f 300 -cf 0.999 -b 0 --repeat $1
    #python main.py -r 20 -t 14 -f 100 -cf 0.999 -b 0 --repeat $1
    #python main.py -r 30 -t 20 -f 100 -cf 0.999 --repeat $1
    #python main.py -r 30 -t 100 -f 100 -cf 0.999 -b 0 --repeat $1
    #python main.py -r 40 -t 20 -f 100 -cf 0.999 --repeat $1
    #python main.py -r 40 -t 100 -f 100 -cf 0.999 -b 0 --repeat $1
    #python main.py -r 42 -t 20 -f 100 -cf 0.999 -b 0 --repeat $1
    #python main.py -r 45 -t 100 -f 100 -cf 0.999 -b 0 --repeat $1
else
    echo "Parametr dotyczacy liczby powtorze jest pusty"
fi
echo "Nacisnij dowolny klawisz by zakonczyc"
while [ true ] ; do
read -t 3 -n 1
if [ $? = 0 ] ; then
exit ;
fi
done