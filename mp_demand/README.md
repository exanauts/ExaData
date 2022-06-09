# Multi-period data generation

`rt_hourlysysload_20181002_20181009.csv` contains the hourly system load data (168 entries)
from 7 AM Oct 2 to 6 AM Oct 9 in 2018.
The data was downloaded from the [ISO New England website](https://www.iso-ne.com/isoexpress/web/reports/load-and-demand/).
In the file rows starting with "D" correspond to the system load for each hour.
For example, the line with `"D","10/02/2018","07",12297.25` indicates that
the load at 7 AM on Oct 2 2018 was 12297.25.

We generate scaling factors from the file by dividing each demand by
the first demand in time.
The following command will print out scaling factors.

```bash
$ python get_load.py rt_hourlysysload_20181002_20181009.csv > scaling_factors.txt
```

These scaling factors are computed hourly.
If you want to apply finer scale, then use `interpolate.py` in the following way:
```bash
$ python interpolate.py scaling_factors.txt 60
```
The above interpolates each hour to compute scaling factors for each minute.
As a result, we have 168*60 = 10080 scaling factors.
A new file will be generated containing these factors with name `scaling_factors_mult_by_60.txt`.

We can apply these scaling factors to generate (hourly, minute-by-minute, or second-by-second) loads over a week for a power network.
The following command will generate real and reactive loads for the case with names
`case_numscales.Pd` and `case_numscales.Qd`, respectively, where `numscales` is an integer denoting the number of time periods in the file.

```bash
$ python interpolate_load.py case.m scaling_factors_mult_by_60.txt
```

## Downloading time-series data for renewable generation

Because of the large file size (> 10MB), we put links to download each time-series data here.
The entire renewable time-series data is available at [here](https://github.com/GridMod/RTS-GMLC/tree/master/RTS_Data/timeseries_data_files).
Links to individual data are below:

- [`DAY_AHEAD_pv.csv`: forecasted available energy generation for each utility scale PV plant by hour](https://raw.githubusercontent.com/GridMod/RTS-GMLC/master/RTS_Data/timeseries_data_files/PV/DAY_AHEAD_pv.csv)
- [`REAL_TIME_pv.csv`: actual available energy generation for each utility scale PV plant by 5-minute interval](https://raw.githubusercontent.com/GridMod/RTS-GMLC/master/RTS_Data/timeseries_data_files/PV/REAL_TIME_pv.csv)
- [`DAY_AHEAD_rtpv.csv`: forecasted energy generation for each rooftop PV plant hour](https://raw.githubusercontent.com/GridMod/RTS-GMLC/master/RTS_Data/timeseries_data_files/RTPV/DAY_AHEAD_rtpv.csv)
- [`REAL_TIME_rtpv.csv`: actual energy generation for each rooftop PV plant by 5-minute interval](https://raw.githubusercontent.com/GridMod/RTS-GMLC/master/RTS_Data/timeseries_data_files/RTPV/REAL_TIME_rtpv.csv)
- [`DAY_AHEAD_wind.csv`: forecasted available energy generation for each wind plant by hour](https://raw.githubusercontent.com/GridMod/RTS-GMLC/master/RTS_Data/timeseries_data_files/WIND/DAY_AHEAD_wind.csv)
- [`REAL_TIME_wind.csv`: actual available energy generation for each wind plant by 5-minute interval](https://raw.githubusercontent.com/GridMod/RTS-GMLC/master/RTS_Data/timeseries_data_files/WIND/REAL_TIME_wind.csv)
- [`DAY_AHEAD_Natural_Inflow.csv`: the solar power potential of the CSP plant by hour](https://raw.githubusercontent.com/GridMod/RTS-GMLC/master/RTS_Data/timeseries_data_files/CSP/DAY_AHEAD_Natural_Inflow.csv)
- [`DAY_AHEAD_hydro.csv`: the hydro power output for each hydro plant by hour](https://raw.githubusercontent.com/GridMod/RTS-GMLC/master/RTS_Data/timeseries_data_files/Hydro/DAY_AHEAD_hydro.csv)
- [`REAL_TIME_hydro.csv`: the hydro power output for each hydro plant by 5-minute interval](https://raw.githubusercontent.com/GridMod/RTS-GMLC/master/RTS_Data/timeseries_data_files/Hydro/REAL_TIME_hydro.csv)

