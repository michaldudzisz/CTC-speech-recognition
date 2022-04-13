#! /usr/bin/bash

dir=`dirname $0`

train_audios="$dir/train_audio_files.scp"
test_audios="$dir/test_audio_files.scp"

train_features="$dir/train_features_files.scp"
test_features="$dir/test_features_files.scp"

train_mapping_file="$dir/train.scp"
test_mapping_file="$dir/test.scp"

mvstats_dir="$dir/mvstats"

target_features_path="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )/features"

./$dir/find_audios.sh

if test -f "$train_mapping_file"; then rm $train_mapping_file; fi
if test -f "$test_mapping_file"; then rm $test_mapping_file; fi
if test -d "$target_features_path"; then rm -r $target_features_path; fi
if test -f "$train_features"; then rm $train_features; fi
if test -f "$test_features"; then rm $test_features; fi

# TODO 10% zbioru uczącego zróbmy na cv

while IFS= read -r line
do
    directory_path=$(dirname "$line")
    dir_file=$(basename "$directory_path")_$(basename "$line")
    filename=$dir_file
    echo "$line $target_features_path/${filename%.WAV.wav}".mfcc >> $train_mapping_file
    echo "$target_features_path/${filename%.WAV.wav}".mfcc >> $train_features
done < "$train_audios"

while IFS= read -r line
do
    directory_path=$(dirname "$line")
    dir_file=$(basename "$directory_path")_$(basename "$line")
    filename=$dir_file
    echo "$line $target_features_path/${filename%.WAV.wav}".mfcc >> $test_mapping_file
    echo "$target_features_path/${filename%.WAV.wav}".mfcc >> $test_features
done < "$test_audios"


export HCONFIG=~/Documents/CTC-speech-recognition/preprocessing/htk_config/main_hconfig
mkdir $dir/features
HCopy -T 1 -C "$dir/htk_config/config" -S "$train_mapping_file"
HCopy -T 1 -C "$dir/htk_config/config" -S "$test_mapping_file"

# in case sth is wrong with htk parameter: main_hconfig <- SOURCEFORMAT = WAV

if test -d "$mvstats_dir"; then rm -r $mstats_dir; fi
mkdir $mvstats_dir

all_features="$dir/all_features"
if test -f "$all_features"; then rm $all_features; fi

cat $train_features >> $all_features
cat $test_features >> $all_features

HCompV -A -D -T 1 -c "$mvstats_dir" -k *.%%%% -q mv -S $all_features
mv $mvstats_dir/mfcc $mvstats_dir/stat
