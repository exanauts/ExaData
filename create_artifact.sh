# #!/bin/bash
# # Script to create Artifact tarball
# # Execute in ../ExaData with `ExaData/create_artifact.sh`

if [ ! -d "ExaData" ]
then
    echo "Could not find 'ExaData' folder"
    exit 1
fi

cd ExaData; hash=`git rev-parse --short HEAD`; cd ..
filename=ExaData-$hash.tar.gz
tar --exclude='.gitignore' --exclude='Manifest.toml' --exclude='Project.toml' --exclude='create_toml.jl' --exclude='create_artifact.sh' --exclude='ExaData/.git' -cvzf $filename ExaData

if [ ! -f "$filename" ]
then
    exit 1
fi


cd ExaData
julia --project create_toml.jl $filename
exit 0