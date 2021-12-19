#! /usr/bin/bash

dir=`dirname $0`
phn_list="$dir/phn_files.scp"
ref61="$dir/ref61.mlf"

if test -f "$ref61"; then rm "$ref61"; fi
if test -f "$phn_list"; then rm "$phn_list"; fi

find ~/timit/timit/data/TRAIN/ -type f -name "*.PHN" >> $phn_list
find ~/timit/timit/data/TEST/ -type f -name "*.PHN" >> $phn_list

while IFS= read -r file
do
    directory_path=$(dirname "$file")
    dir_file=$(basename "$directory_path")/$(basename "$file")
    echo "\"*/$dir_file\"" >> "$ref61"
    cat $file >> "$ref61"
    echo "." >> "$ref61"
done < "$phn_list"

