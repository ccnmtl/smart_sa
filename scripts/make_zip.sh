#!/bin/bash

mkdir ziptmp
cd ziptmp
git clone git@git.ccnmtl.columbia.edu:smart_sa.git
rm -rf smart_sa/.git
zip masivukeni.zip -r smart_sa
cd ..
mv ziptmp/masivukeni.zip .
rm -rf ziptmp

