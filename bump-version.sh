#! /bin/bash

function update_release {
    FILENAME=$1
    RELEASE=$2
    mv $FILENAME $FILENAME.tmp
    sed -e "s/release = .*/release = \"$RELEASE\"/g" $FILENAME.tmp > $FILENAME
    rm $FILENAME.tmp
    chmod u+x $FILENAME
}

if [ "$1" == "" ]; then
    echo "Error: the version number must be passed as argument"
    exit 2
fi

update_release "kvkwebscraper.py" $1
update_release "service.py" $1
