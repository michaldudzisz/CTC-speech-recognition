#! /usr/bin/sh

find ~/timit/timit/data/TRAIN/ -type f -name "*.wav" > train_audio_files.scp
find ~/timit/timit/data/TEST/ -type f -name "*.wav" > test_audio_files.scp
