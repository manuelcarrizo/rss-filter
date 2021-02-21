#!/bin/bash

do_activate() {
    if [ -f venv/bin/activate ] ;
    then 
        source venv/bin/activate
    fi
}

do_venv() {
    if [ ! -d venv ] ;
    then 
        virtualenv venv
    fi
}

CURRENT_PATH=`dirname ${BASH_SOURCE}`
CONFIG=$1

do_venv
do_activate

cd $CURRENT_PATH

pip install -r requirements.txt

python filter.py $CONFIG | python upload.py $CONFIG