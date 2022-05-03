#! /usr/bin/sh

# dir=`dirname $0`

# train_audios="$dir/train_audio_files.scp"

# dataset_path = 

# input="$dir/../config/to/txt/file"
# while IFS= read -r line
# do
#   echo "$line"
# done < "$input"

find ~/Documents/timit/timit/data/TRAIN/ -type f -name "*.wav" > train_audio_files.scp
find ~/Documents/timit/timit/data/TEST/ -type f -name "*.wav" > test_audio_files.scp
