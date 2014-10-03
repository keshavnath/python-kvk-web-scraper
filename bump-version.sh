#! /bin/bash

if [ "$1" == "" ]; then
    echo "Error: the version number must be passed as argument"
    exit 2
fi

mv kvkwebscraping.py kvkwebscraping.py.tmp
sed -e "s/version = .*/version = $1/g" kvkwebscraping.py.tmp > kvkwebscraping.py
rm kvkwebscraping.py.tmp
chmod u+x kvkwebscraping.py
