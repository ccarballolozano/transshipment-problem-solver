# transshipment-problem-solver

transshipment-problem-solver is a solver for the transshipment problem which allows loading the problem based on the distances between points via Google Maps Distance Matrix API.

## Running instructions

1. Run transshipment-problem-solver to open the GUI
  
2. Buid data

   Provide the data where requested and then push the button.
   
   - Origins: A csv file with data of the origins.
     ```
     name,latitude,longitude,supply,costperkm
     Bilbao Spain,,,4000,1
     Paris France,,,3000,1.5
     Berlin Germany,,,3000,2
     ```
   - Transshipments: A csv file with data of the transshipments.
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

3. Edit data
   
   If you want to edit any data that was built at step 2, open the file and edit manually. A typical edit would be to restrict the amount of goods that can be sent from an origin/transshipment to a transshipment/destination, also called capacities, since all are set to infinity by default.
   
   For example, to set the capacity from the origin Bilbao to the transshipment Toulouse to 2000, open the file capacity_origins_to_transshipments.csv, which by default looks like  
   ```
   ,Zaragoza,Oporto,Toulouse,Lyon,Turin,Francfort,Zurich
   Bilbao,inf,inf,inf,inf,inf,inf,inf
   Paris,inf,inf,inf,inf,inf,inf,inf
   Berlin,inf,inf,inf,inf,inf,inf,inf
   ```
   and modify the desired capacity, in our particular case
   ```
   ,Zaragoza,Oporto,Toulouse,Lyon,Turin,Francfort,Zurich
   Bilbao,inf,inf,2000,inf,inf,inf,inf
   Paris,inf,inf,inf,inf,inf,inf,inf
   Berlin,inf,inf,inf,inf,inf,inf,inf
   ```
  Now, even if Bilbao had a supply of 4000, it could only send to Toulouse maximum amount of 2000.
  
  Note 1: Be careful if you edit the names (not recommended), since those will have to coincide at every file.
  
  Note 2: To get an integer solution, do not set capacities to non integer quantities (which actually would not really make sense).
  
4. Get the optimal solution

   Push the button to solve the problem. If everything went well, a success message will appear.
   
   Frequent non success results include.
   
   - Problem infeasible:
   
     - Supply is not greater than demand, so requirements cannot be satisfied.
     - Supply is greater than demand, but because of the capacities some points cannot receive all the required demand.
     - Some connections are not well: point not well defined (e.g., Bilbao is not valid since they are multiple places, so we put Bilbao Spain or Bilbao Basque Country Spain) or a path not possible by car (e.g., from New York to . 

5. Export results
   
   Choose folder and name (without extension) to export the results and push to .csv and/or to .xls to get the results file(s) in the desired location.

## Alternative usage

It is not necessary to work using the Google Maps DistanceMatrix API. Actually, this step's goal is to create the necessary files to run the program by taking into account the distances and costs between points. 

If you want to create your custom files (costs, capacities, ...) just skip the build data step and start at step 3, in edit data. In the opened folder, you need to create/paste the necessary files, that are:
  
  * id_origins.csv
  * id_destinations.csv
  * id_transshipments.csv
  * cost_origins_to_destinations.csv
  * cost_origins_to_transshipments.csv
  * cost_transshipments_to_destinations.csv
  * cost_transshipments_to_transshipments.csv
  * supply_origins.csv
  * supply_transshipments.csv
  * demand_destinations.csv
  * demand_transshipments.csv
  * capacity_origins_to_destinations.csv
  * capacity_origins_to_transshipments.csv
  * capacity_transshipments_to_destinations.csv
  * capacity_transshipments_to_transshipments.csv

Take a look to the folder examples/input_for_direct_add to see the structure of the files or you can see the files created when building from the Buid data step.

## Generated data

When running the program, some data is automatically generated (apart from the input data):

* data_out/
  * opt_all.csv
  * opt_all.xlsx
  * opt_origins_to_destinations.csv
  * opt_origins_to_transshipments.csv
  * opt_transshipments_to_destinations.csv
  * opt_transshipments_to_transshipments.csv
