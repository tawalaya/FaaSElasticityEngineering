#! /bin/sh

. scripts/config.sh

echo "copy to $(host)"
rsync -r -P --exclude=.git/ --exclude=node_modules/ --exclude=reports $(pwd) $(host):
echo "done."