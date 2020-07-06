#! /bin/sh

. scripts/config.sh

target=${PWD##*/} 
echo "copy from $host to results"
scp $host:$target/scripts/config.sh "scripts/config_$(date -I).sh"
rsync -P -u -r $host:$target/results . 
echo "done."