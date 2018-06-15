# transshipment-problem-solver

transshipment-problem-solver is a solver for the transshipment problem solver which allows loading the problem based on the distances between points via Google Maps Distance Matrix API.

The running instructions are the following.

Input data that must be provided to the algorithm is:

* data_in/
  * cost_origins_to_destinations.csv
  * cost_origins_to_transshipments.csv
  * cost_transshipments_to_destinations.csv
  * cost_transshipments_to_transshipments.csv
  * production_origins.csv
  * production_transshipments.csv
  * demand_destinations.csv
  * demand_transshipments.csv
  
Optional files are

* data_in/
  * id_origins.csv
  * id_destinations.csv
  * id_transshipments.csv
 
To use the Google Maps Distance Matrix API method, the files that must be provided are different, and will automatically create the previous ones. The files that are needed are:

* data_in/
  * origins.csv
  * destinations.csv
  * transshipments.csv

* distancematrix_api_key.txt

To run the algorithm from manually added data, call

```bash
python transshipment-problem-solver.py
```

To run the algorithm in the maps mode, call
``` bash
python transshipment-problem-solver -g "maps"
```

The alworithm outputs the results

* data_out/
  * opt_all.csv
  * opt_all.xlsx
  * opt_origins_to_destinations.csv
  * opt_origins_to_transshipments.csv
  * opt_transshipments_to_destinations.csv
  * opt_transshipments_to_transshipments.csv
