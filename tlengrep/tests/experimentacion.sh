#!/bin/bash

cd ..

echo " ***** EXPERIMENTACIÓN SOBRE LA CANTIDAD DE CADENAS *****"
echo ""

echo "--- con nuestro código ---"
for i in tests/strings/cantidad_de_cadenas/* 
do
    echo ""
    echo "Procesando archivo $i"
    python3 tlengrep.py tests.regexes.r29 $i -m
done

echo ""
echo "--- con el código naive ---"
for i in tests/strings/cantidad_de_cadenas/* 
do
    echo ""
    echo "Procesando archivo $i"
    python3 tlengrep.py tests.regexes.r29 $i -m -n
done

echo ""

echo " ***** EXPERIMENTACIÓN SOBRE LA LONGITUD DE LA CADENA *****"
echo ""

echo "--- con nuestro código ---"
for i in tests/strings/longitud_de_cadena/* 
do
    echo ""
    echo "Procesando archivo $i"
    python3 tlengrep.py tests.regexes.r29 $i -m
done

echo ""
echo "--- con el código naive ---"
for i in tests/strings/longitud_de_cadena/* 
do
    echo ""
    echo "Procesando archivo $i"
    python3 tlengrep.py tests.regexes.r29 $i -m -n
done


echo ""




echo " ***** SOLO PARA FLEXEAR *****"
echo ""

echo "--- con nuestro código ---"
for i in tests/strings/too_big_4_u/* 
do
    echo ""
    echo "Procesando archivo $i"
    python3 tlengrep.py tests.regexes.r29 $i -m
done