#! /usr/bin/bash

dir=`dirname $0`
htk_config=$dir/../../preprocessing/htk_config

export HCONFIG=$htk_config/main_hconfig
HCopy -T 1 -C "$htk_config/config" -S "$dir/tmp/spotting.scp"

HCompV -A -D -T 1 -c "$dir/tmp" -k *.%%%% -q mv -S "$dir/tmp/spotting_feature.scp"
mv $dir/tmp/mfcc $dir/tmp/stat
