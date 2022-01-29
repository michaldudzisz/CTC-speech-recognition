#! /usr/bin/sh

find ~/Documents/timit/timit/data/TRAIN/ -type f -name "*.wav" > train_audio_files.scp
find ~/Documents/timit/timit/data/TEST/ -type f -name "*.wav" > test_audio_files.scp
