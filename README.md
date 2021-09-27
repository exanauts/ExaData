This repository contains the MATPOWER file for the TAMU2000 case with hurricane scenarios created by NREL
1. **``case_ACTIVSg2000.m``** contains the network details
1. **``case_ACTIVSg2000.Pd``** contains the Active Power data for 3600 periods
1. **``case_ACTIVSg2000.Qd``** contains the Reactive Power data for 3600 periods
1. **``case_ACTIVSg2000.Ctgs_random``** contains random line contingencies used for development
1. **``case_ACTIVSg2000.Ctgs``** contains feasible line contingencies run through [PowerModels.jl](https://github.com/lanl-ansi/PowerModels.jl/)

## Funding
This research was supported by the Exascale Computing Project (17-SC-20-SC), a joint project of the U.S. Department of Energy’s Office of Science and National Nuclear Security Administration, responsible for delivering a capable exascale ecosystem, including software, applications, and hardware technology, to support the nation’s exascale computing imperative.
