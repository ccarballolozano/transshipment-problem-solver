# transshipment-problem-solver

transshipment-problem-solver is a solver for the transshipment problem which allows loading the problem based on the distances between points via Google Maps Distance Matrix API.

## Running instructions

1. Run transshipment-problem-solver to open the GUI
  
2. Buid data

   Provide the data where requested.
   
   - Origins: A csv file with data of the origins.
     ```
     name,latitude,longitude,supply,costperkm
     Bilbao Spain,,,4000,1
     Paris France,,,3000,1.5
     Berlin Germany,,,3000,2
     ```
   - Transshipments: A csv file with data of the transsipments.
     ```
     name,latitude,longitude,supply,demand,costperkm
     Zaragoza Spain,,,1275,900,0.5
     Oporto Portugal,,,1000,800,0.5
     Toulouse France,,,1300,1000,0.75
     Lyon France,,,750,950,0.75
     Turin Italy,,,500,800,0.5
     Francfort Germany,,,1100,825,1
     Zurich Suiza,,,500,600,1.5
     ```
   - Destinations: A csv file with data of the destinations.
     ```
     name,latitude,longitude,demand
     Carballo Spain,,,750
     Zamora Spain,,,1500
     Burdeos France,,,2000
     Verona Italy,,,1000
     Ausburgo Germany,,,2150
     Amsterdam Netherlands,,,1100   
     ```
   - DistanceMatrix API key: A string with the Google Maps DistanceMatrix API Key
     ```
     AIzaSyDr5Qu04svd-pbBOJmlhFdLhLtwkwt_pic
     ```
    
    Note 1: Respect the structure of the csv files (commas, spacing,...).
    
    Note 2: "latitude" and "longitude" is not provided because "name" is enough to run. The longer the name, the better for the software.
    
    Note 3: The API key I provide is my free one, so can be used with limitations. Better to get your own one.

---------

* data_in/
  * id_origins.csv
  * id_destinations.csv
  * id_transshipments.csv
  * capacity_origins_to_destinations.csv
  * capacity_origins_to_transshipments.csv
  * capacity_transshipments_to_destinations.csv
  * capacity_transshipments_to_transshipments.csv
 
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
python transshipment-problem-solver.py -g "maps"
```

The algorithm outputs the results

* data_out/
  * opt_all.csv
  * opt_all.xlsx
  * opt_origins_to_destinations.csv
  * opt_origins_to_transshipments.csv
  * opt_transshipments_to_destinations.csv
  * opt_transshipments_to_transshipments.csv
