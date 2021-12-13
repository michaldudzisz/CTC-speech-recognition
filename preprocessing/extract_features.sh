#! /usr/bin/bash

dir=`dirname $0`

train_audios="$dir/train_audio_files.scp"
test_audios="$dir/test_audio_files.scp"

train_mapping_file="$dir/train.scp"
test_mapping_file="$dir/test.scp"

target_features_path="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )/features"

./$dir/find_audios.sh

if test -f "$train_mapping_file"; then rm $train_mapping_file; fi
if test -f "$test_mapping_file"; then rm $test_mapping_file; fi
if test -d "$target_features_path"; then rm -r $target_features_path; fi

while IFS= read -r line
do
    filename=`basename $line`
    echo "$line $target_features_path/${filename%.WAV.wav}".mfcc >> $train_mapping_file
done < "$train_audios"

while IFS= read -r line
do
    filename=`basename $line`
    echo "$line $target_features_path/${filename%.WAV.wav}".mfcc >> $test_mapping_file
done < "$test_audios"


export HCONFIG=~/projects/CTC-speech-recognition/preprocessing/htk_config/main_hconfig
mkdir $dir/features
HCopy -T 1 -C "$dir/htk_config/config" -S "$train_mapping_file"
