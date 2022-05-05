#!/bin/bash

dir=`dirname $0`

result61_file=$dir/tmp/result61.mlf
result39_file=$dir/tmp/result39.mlf

HLEd -A -T 1 -X rec -i $result39_file $dir/../../timit2_39.led $result61_file 

oldsize=""
while newsize=`wc -c $result39_file`; [ "$oldsize" != "$newsize" ]; do
   oldsize=$newsize
   HLEd -X rec -i temp.mlf ./mergesil.led $result39_file
   mv temp.mlf $result39_file
done
