#! /usr/bin/sh

# dir=`dirname $0`

# train_audios="$dir/train_audio_files.scp"

# dataset_path = 

# input="$dir/../config/to/txt/file"
# while IFS= read -r line
# do
#   echo "$line"
# done < "$input"
path=$1
train_path=$path/data/TRAIN
test_path=$path/data/TEST

find $train_path -type f -name "*.wav" > train_audio_files.scp
find $test_path -type f -name "*.wav" > test_audio_files.scp
