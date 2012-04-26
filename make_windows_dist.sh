#!/bin/bash

rm -rf /mnt/key/smart_sa
rsync -a -z -C --delete --verbose --exclude '*~' --exclude ve --exclude .git --exclude '*.pyc' ../smart_sa /mnt/key/

