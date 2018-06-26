import pandas as pd
import numpy as np
import urllib
import os
import json
import csv


def from_maps_api(api_key, origins_file, destinations_file, transshipments_file, to_folder):
    if not os.path.isdir(to_folder):
        os.mkdir(to_folder)
    else:
        pass
    o_df = pd.read_csv(origins_file)
    o_name = o_df['name']
    o_lat = o_df['latitude']
    o_long = o_df['longitude']
    o_supply = o_df['supply']
    o_cost = o_df['costperkm']
    d_df = pd.read_csv(destinations_file)
    d_name = d_df['name']
    d_lat = d_df['latitude']
    d_long = d_df['longitude']
    d_demand = d_df['demand']
    t_df = pd.read_csv(transshipments_file)
    t_name = t_df['name']
    t_lat = t_df['latitude']
    t_long = t_df['longitude']
    t_supply = t_df['supply']
    t_demand = t_df['demand']
    t_cost = t_df['costperkm']
    del o_df, d_df, t_df
    # Now get distance matrix via google maps API
    # by name, distancematrix is requested as
    # url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins=Seattle&destinations=San+Francisco&mode=driving&sensor=false"
    # by latitude and longitude, distancematrix is requested by
    # Origins to destinations
    o_to_d = np.zeros(shape=(len(o_name), len(d_name)))  # cost
    o_to_d_cap = np.full((len(o_name), len(d_name)), np.inf)  # capacity
    for i in range(len(o_name)):
        if pd.isna(o_cost[i]):
            cost_per_km = 1
        else:
            cost_per_km = o_cost[i]        
        if pd.isna(o_name.iloc[i]):
            url_origin = str(o_lat[i]) + ',' + str(o_long[i])
        else:
            url_origin = str(o_name[i]).replace(' ', '+')
        for j in range(len(d_name)):
            if pd.isna(d_name.iloc[j]):
                url_destination = str(d_lat[j]) + ',' + str(d_long[j])
            else:
                url_destination = str(d_name[j]).replace(' ', '+')
            url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=%s&destinations=%s&mode=driving&sensor=false&key=%s' % (
                url_origin, url_destination, api_key)
            r = urllib.request.urlopen(url).read().decode('utf8')
            json_data = json.loads(r)
            if json_data['rows'][0]['elements'][0]['status'] == "ZERO_RESULTS":
                distance = 0
                o_to_d_cap[i, j] = 0
            else:
                distance = json_data['rows'][0]['elements'][0]['distance']['value']
            o_to_d[i, j] = cost_per_km * distance / 1000
    # Origins to transshipments
    o_to_t = np.zeros(shape=(len(o_name), len(t_name)))
    o_to_t_cap = np.full((len(o_name), len(t_name)), np.inf)
    for i in range(len(o_name)):
        if pd.isna(o_cost[i]):
            cost_per_km = 1
        else:
            cost_per_km = o_cost[i]
        if pd.isna(o_name.iloc[i]):
            url_origin = str(o_lat[i]) + ',' + str(o_long[i])
        else:
            url_origin = str(o_name[i]).replace(' ', '+')
        for j in range(len(t_name)):
            if pd.isna(t_name.iloc[j]):
                url_destination = str(d_lat[j]) + ',' + str(d_long[j])
            else:
                url_destination = str(t_name[j]).replace(' ', '+')
            url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=%s&destinations=%s&mode=driving&sensor=false&key=%s' % (
                url_origin, url_destination, api_key)
            r = urllib.request.urlopen(url).read().decode('utf8')
            json_data = json.loads(r)
            if json_data['rows'][0]['elements'][0]['status'] == "ZERO_RESULTS":
                distance = 0
                o_to_t_cap[i, j] = 0
            else:
                distance = json_data['rows'][0]['elements'][0]['distance']['value']
            o_to_t[i, j] = cost_per_km * distance / 1000
    # Transshipments to destinations
    t_to_d = np.zeros(shape=(len(t_name), len(d_name)))
    t_to_d_cap = np.full((len(t_name), len(d_name)), np.inf)    
    for i in range(len(t_name)):
        if pd.isna(t_cost[i]):
            cost_per_km = 1
        else:
            cost_per_km = t_cost[i]
        if pd.isna(t_name.iloc[i]):
            url_origin = str(t_lat[i]) + ',' + str(t_long[i])
        else:
            url_origin = str(t_name[i]).replace(' ', '+')
        for j in range(len(d_name)):
            if pd.isna(d_name.iloc[j]):
                url_destination = str(d_lat[j]) + ',' + str(d_long[j])
            else:
                url_destination = str(d_name[j]).replace(' ', '+')
            url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=%s&destinations=%s&mode=driving&sensor=false&key=%s' % (
                url_origin, url_destination, api_key)
            r = urllib.request.urlopen(url).read().decode('utf8')
            json_data = json.loads(r)
            if json_data['rows'][0]['elements'][0]['status'] == "ZERO_RESULTS":
                distance = 0
                t_to_d_cap[i, j] = 0
            else:
                distance = json_data['rows'][0]['elements'][0]['distance']['value']
            t_to_d[i, j] = cost_per_km * distance / 1000
    # Transshipments to transshipments
    t_to_t = np.zeros(shape=(len(t_name), len(t_name)))
    t_to_t_cap = np.full((len(t_name), len(t_name)), np.inf)
    for i in range(len(t_name)):
        if pd.isna(t_cost[i]):
            cost_per_km = 1
        else:
            cost_per_km = t_cost[i]
        if pd.isna(t_name.iloc[i]):
            url_origin = str(t_lat[i]) + ',' + str(t_long[i])
        else:
            url_origin = str(t_name[i]).replace(' ', '+')
        for j in range(len(t_name)):
            if j == i:  # zero distance
                next
            if pd.isna(t_name.iloc[j]):
                url_destination = str(t_lat[j]) + ',' + str(t_long[j])
            else:
                url_destination = str(t_name[j]).replace(' ', '+')
            url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=%s&destinations=%s&mode=driving&sensor=false&key=%s' % (
                url_origin, url_destination, api_key)
            r = urllib.request.urlopen(url).read().decode('utf8')
            json_data = json.loads(r)
            if json_data['rows'][0]['elements'][0]['status'] == "ZERO_RESULTS":
                distance = 0
                t_to_t_cap[i, j] = 0
            else:
                distance = json_data['rows'][0]['elements'][0]['distance']['value']
            t_to_t[i, j] = cost_per_km * distance / 1000
    # Remove existing files
    for f in os.listdir(to_folder):
        if f.endswith(".csv"):
            os.remove(os.path.join(to_folder, f))
    """
    # Write cost values
    np.savetxt(os.path.join(to_folder, "cost_origins_to_destinations.csv"), o_to_d, fmt="%f", delimiter=",")
    np.savetxt(os.path.join(to_folder, "cost_origins_to_transshipments.csv"), o_to_t, fmt="%f", delimiter=",")
    np.savetxt(os.path.join(to_folder, "cost_transshipments_to_destinations.csv"), t_to_d, fmt="%f", delimiter=",")
    np.savetxt(os.path.join(to_folder, "cost_transshipments_to_transshipments.csv"), t_to_t, fmt="%f", delimiter=",")
    # Write supplies and demands
    np.savetxt(os.path.join(to_folder, "production_origins.csv"), o_supply.values, fmt="%f", delimiter=",")
    np.savetxt(os.path.join(to_folder, "production_transshipments.csv"), t_supply.values, fmt="%f", delimiter=",")
    np.savetxt(os.path.join(to_folder, "demand_destinations.csv"), d_demand.values, fmt="%f", delimiter=",")
    np.savetxt(os.path.join(to_folder, "demand_transshipments.csv"), t_demand.values, fmt="%f", delimiter=",")
    # Write capacities
    np.savetxt(os.path.join(to_folder, "capacity_origins_to_destinations.csv"), o_to_d_cap, fmt="%f", delimiter=",")
    np.savetxt(os.path.join(to_folder, "capacity_origins_to_transshipments.csv"), o_to_t_cap, fmt="%f", delimiter=",")
    np.savetxt(os.path.join(to_folder, "capacity_transshipments_to_destinations.csv"), t_to_d_cap, fmt="%f", delimiter=",")
    np.savetxt(os.path.join(to_folder, "capacity_transshipments_to_transshipments.csv"), t_to_t_cap, fmt="%f", delimiter=",")
    """
    # Write names
    o_id = []
    d_id = []
    t_id = []
    for i in range(len(o_name)):
        if pd.isna(o_name[i]):
            o_id.append(str(o_lat[i]) + ' ' + str(o_long[i]))
        else:
            o_id.append(str(o_name[i].split(' ', 1)[0]))
    for i in range(len(d_name)):
        if pd.isna(d_name[i]):
            d_id.append(str(d_lat[i]) + ' ' + str(d_long[i]))
        else:
            d_id.append(str(d_name[i].split(' ', 1)[0]))
    for i in range(len(t_name)):
        if pd.isna(t_name[i]):
            t_id.append(str(t_lat[i]) + ' ' + str(t_long[i]))
        else:
            t_id.append(str(t_name[i].split(' ', 1)[0]))
    with open(os.path.join(to_folder, "id_origins.csv"), "w") as f:
        out = csv.writer(f, delimiter=',')
        out.writerow(o_id)
    with open(os.path.join(to_folder, "id_destinations.csv"), "w") as f:
        out = csv.writer(f, delimiter=',')
        out.writerow(d_id)
    with open(os.path.join(to_folder, "id_transshipments.csv"), "w") as f:
        out = csv.writer(f, delimiter=',')
        out.writerow(t_id)
    # Write cost values
    pd.DataFrame(o_to_d, index=o_id, columns=d_id).to_csv(
        os.path.join(to_folder, "cost_origins_to_destinations.csv"))
    pd.DataFrame(o_to_t, index=o_id, columns=t_id).to_csv(
        os.path.join(to_folder, "cost_origins_to_transshipments.csv"))
    pd.DataFrame(t_to_d, index=t_id, columns=d_id).to_csv(
        os.path.join(to_folder, "cost_transshipments_to_destinations.csv"))
    pd.DataFrame(t_to_t, index=t_id, columns=t_id).to_csv(
        os.path.join(to_folder, "cost_transshipments_to_transshipments.csv"))
    # Write supplies and demands
    pd.DataFrame(o_supply.values, index=o_id, columns=["supply"]).to_csv(
        os.path.join(to_folder, "supply_origins.csv"))
    pd.DataFrame(t_supply.values, index=t_id, columns=["supply"]).to_csv(
        os.path.join(to_folder, "supply_transshipments.csv"))
    pd.DataFrame(d_demand.values, index=d_id, columns=["demand"]).to_csv(
        os.path.join(to_folder, "demand_destinations.csv"))
    pd.DataFrame(t_demand.values, index=t_id, columns=["demand"]).to_csv(
        os.path.join(to_folder, "demand_transshipments.csv"))
    # Write capacities
    pd.DataFrame(o_to_d_cap, index=o_id, columns=d_id).to_csv(
        os.path.join(to_folder, "capacity_origins_to_destinations.csv"))
    pd.DataFrame(o_to_t_cap, index=o_id, columns=t_id).to_csv(
        os.path.join(to_folder, "capacity_origins_to_transshipments.csv"))
    pd.DataFrame(t_to_d_cap, index=t_id, columns=d_id).to_csv(
        os.path.join(to_folder, "capacity_transshipments_to_destinations.csv"))
    pd.DataFrame(t_to_t_cap, index=t_id, columns=t_id).to_csv(
        os.path.join(to_folder, "capacity_transshipments_to_transshipments.csv"))
    return
