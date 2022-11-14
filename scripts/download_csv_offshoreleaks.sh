
#!/bin/bash

DIR=$PWD
URL_BASE=https://github.com/ICIJ/offshoreleaks-data-packages/raw/main/raw-data
DIR_IMPORT_CSV=$PWD/db/import

declare -a files=(
    "csv_bahamas_leaks.2017-12-19.zip" 
    "csv_offshore_leaks.2018-02-14.zip"
    "csv_panama_papers.2018-02-14.zip"
    "csv_paradise_papers.2018-02-14.zip"
)

for filee in ${files[*]}; do
    if [[ -e "$DIR/$filee" ]] ; then
    echo "O $filee arquivo já existe"
    else
    wget -P $DIR $URL_BASE/$filee
    unzip $DIR/$filee
    mv $DIR/*.csv $DIR_IMPORT_CSV/
    fi
done

ls .
# wget -P $DIR $URL_BASE/csv_bahamas_leaks.2017-12-19.zip

# file csv_bahamas_leaks.2017-12-19.zip