# ExaData

This repository contains all the data files used by the exanauts group for the ExaSGD ECP project.

## Using the Artifact
Download the latest `Artifact.toml` at https://github.com/exanauts/ExaData/releases and put it in your project folder. The folder structure inside the artifact will be linked to the tagged release version in this repository.

```julia
using LazyArtifacts
datafile = joinpath(artifact"ExaData", "ExaData", "matpower", "case2868rte.m")
println("Path to artifact file: $datafile")
```

## Creating a new artifact

The `create_artifact.sh` shell script creates a `ExaData-${COMMIT-HASH}.tar.gz` file and the corresponding `Artifacts.toml` file that needs to be added to projects relying on this artifact.

## MATPOWER files

The folder `matpower` contains all the MATPOWER 7.1 data files.

## Load scenarios and contingencies

The folder `mp_demand` contains various demand/load together with contingency lists for some of the network files.

## TAMU2000 with hurrance scenarios created by NREL
1. **``case_ACTIVSg2000.m``** contains the network details
1. **``mp_demand/case_ACTIVSg2000.Pd``** contains the Active Power data for 3600 periods
1. **``mp_demand/case_ACTIVSg2000.Qd``** contains the Reactive Power data for 3600 periods
1. **``mp_demand/case_ACTIVSg2000.Ctgs_random``** contains random line contingencies used for development
1. **``mp_demand/case_ACTIVSg2000.Ctgs``** contains feasible line contingencies run through [PowerModels.jl](https://github.com/lanl-ansi/PowerModels.jl/)

## Funding
This research was supported by the Exascale Computing Project (17-SC-20-SC), a joint project of the U.S. Department of Energy’s Office of Science and National Nuclear Security Administration, responsible for delivering a capable exascale ecosystem, including software, applications, and hardware technology, to support the nation’s exascale computing imperative.
