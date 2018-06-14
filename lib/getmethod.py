import pandas as pd
import numpy as np
import urllib
import os
import json
import csv


def from_maps_api(cost_per_km, api_key_file, from_folder, to_folder):
    # read distancematrix api key
    with open(api_key_file, 'r') as f:
        api_key = f.readline()
    o_df = pd.read_csv(os.path.join(
        from_folder, "origins.csv"))
    o_name = o_df['name']
    o_lat = o_df['latitude']
    o_long = o_df['longitude']
    o_supply = o_df['supply']
    d_df = pd.read_csv(os.path.join(
        from_folder, "destinations.csv"))
    d_name = d_df['name']
    d_lat = d_df['latitude']
    d_long = d_df['longitude']
    d_demand = d_df['demand']
    t_df = pd.read_csv(os.path.join(
        from_folder, "transshipments.csv"))
    t_name = t_df['name']
    t_lat = t_df['latitude']
    t_long = t_df['longitude']
    t_supply = t_df['supply']
    t_demand = t_df['demand']
    del o_df, d_df, t_df
    # Now get distance matrix via google maps API
    # by name, distancematrix is requested as
    # url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins=Seattle&destinations=San+Francisco&mode=driving&sensor=false"
    # by latitude and longitude, distancematrix is requested by
    # Origins to destinations
    o_to_d = np.zeros(shape=(len(o_name), len(d_name)))
    for i in range(len(o_name)):
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
            # print(url)
            r = urllib.request.urlopen(url).read()
            json_data = json.loads(r)
            distance = json_data['rows'][0]['elements'][0]['distance']['value']
            o_to_d[i, j] = cost_per_km * distance / 1000
    # Origins to transshipments
    o_to_t = np.zeros(shape=(len(o_name), len(t_name)))
    for i in range(len(o_name)):
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
            # print(url)
            r = urllib.request.urlopen(url).read()
            json_data = json.loads(r)
            distance = json_data['rows'][0]['elements'][0]['distance']['value']
            o_to_t[i, j] = cost_per_km * distance
    # Transshipments to destinations
    t_to_d = np.zeros(shape=(len(t_name), len(d_name)))
    for i in range(len(t_name)):
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
            # print(url)
            r = urllib.request.urlopen(url).read()
            json_data = json.loads(r)
            distance = json_data['rows'][0]['elements'][0]['distance']['value']
            t_to_d[i, j] = cost_per_km * distance
    # Transshipments to transshipments
    t_to_t = np.zeros(shape=(len(t_name), len(t_name)))
    for i in range(len(t_name)):
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
            # print(url)
            r = urllib.request.urlopen(url).read()
            json_data = json.loads(r)
            distance = json_data['rows'][0]['elements'][0]['distance']['value']
            t_to_t[i, j] = cost_per_km * distance
    # Write cost functions
    np.savetxt(os.path.join(to_folder, "cost_origins_to_destinations.csv"), o_to_d, fmt="%.5f", delimiter=",")
    np.savetxt(os.path.join(to_folder, "cost_origins_to_transshipments.csv"), o_to_t, fmt="%.5f", delimiter=",")
    np.savetxt(os.path.join(to_folder, "cost_transshipments_to_destinations.csv"), t_to_d, fmt="%.5f", delimiter=",")
    np.savetxt(os.path.join(to_folder, "cost_transshipments_to_transshipments.csv"), t_to_t, fmt="%.5f", delimiter=",")
    # Write supplies and demands
    np.savetxt(os.path.join(to_folder, "production_origins.csv"), o_supply.values, fmt="%.5f", delimiter=",")
    np.savetxt(os.path.join(to_folder, "production_transshipments.csv"), t_supply.values, fmt="%.5f", delimiter=",")
    np.savetxt(os.path.join(to_folder, "demand_destinations.csv"), d_demand.values, fmt="%.5f", delimiter=",")
    np.savetxt(os.path.join(to_folder, "demand_transshipments.csv"), t_demand.values, fmt="%.5f", delimiter=",")
    # Write names
    o_ids = []
    d_ids = []
    t_ids = []
    for i in range(len(o_name)):
        if pd.isna(o_name[i]):
            o_ids.append(str(o_lat[i]) + ' ' + str(o_long[i]))
        else:
            o_ids.append(str(o_name[i]))
    for i in range(len(d_name)):
        if pd.isna(d_name[i]):
            d_ids.append(str(d_lat[i]) + ' ' + str(d_long[i]))
        else:
            d_ids.append(str(d_name[i]))
    for i in range(len(t_name)):
        if pd.isna(t_name[i]):
            t_ids.append(str(t_lat[i]) + ' ' + str(t_long[i]))
        else:
            t_ids.append(str(t_name[i]))
    np.savetxt("ids_origins.csv", o_ids, delimiter=",", fmt='%s')
    np.savetxt("ids_destinations.csv", d_ids, delimiter=",", fmt='%s')
    np.savetxt("ids_transshipments.csv", t_ids, delimiter=",", fmt='%s')
    #out = csv.writer(open(os.join.path(to_folder, "ids_origins.csv"), "w"), delimiter=',', quoting=csv.QUOTE_ALL)
    #out = csv.writer(open(os.join.path(to_folder, "ids_origins.csv"), "w"), delimiter=',', quoting=csv.QUOTE_ALL)
    return
