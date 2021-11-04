#!/bin/bash
# Script to create Artifact tarball
# Execute in ../ExaData with `ExaData/create_artifact.sh`

if [ ! -d "ExaData" ]
then
    echo "Could not find 'ExaData' folder"
    exit 1
fi

cd ExaData; hash=`git rev-parse --short HEAD`; cd ..
tar --exclude='create_artifact.sh' --exclude='ExaData/.git' -cvzf ExaData-$hash.tar.gz ExaData

if [ -f "ExaData-$hash.tar.gz" ]
then
    exit 0
fi
exit 1

