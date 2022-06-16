#!/bin/bash

dir=`dirname $0`

result61_file=$dir/result61-beam-no-lm.mlf # result61_file=$dir/result.mlf
result39_file=$dir/result39.mlf


HLEd -A -T 1 -X rec -i $result39_file ./timit2_39.led $result61_file 

# mv temp.mlf $result_file # TODO nadpisywanie pliku mi się nie podoba

oldsize=""
while newsize=`wc -c $result39_file`; [ "$oldsize" != "$newsize" ]; do
   oldsize=$newsize
   HLEd -X rec -i temp.mlf ./mergesil.led $result39_file
   mv temp.mlf $result39_file
done

#test accuarcy
HResults -I $dir/preprocessing/ref39.mlf /dev/null $result39_file
