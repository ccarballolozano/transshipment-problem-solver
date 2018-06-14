import numpy as np
import os
import pandas as pd


def to_complete_file(out_data_folder, o_names, d_names, t_names):
    rows = o_names + t_names
    cols = d_names + t_names
    df = pd.DataFrame(index=rows, columns=cols)
    data = np.loadtxt(os.path.join(out_data_folder, "opt_origins_to_destinations.csv"),
                      delimiter=",")
    for i in range(data.shape[0]):
        for j in range(data.shape[0]):
            df.loc[o_names[i], d_names[j]] = data[i, j]
    data = np.loadtxt(os.path.join(out_data_folder, "opt_origins_to_transshipments.csv"),
                      delimiter=",")
    for i in range(data.shape[0]):
        for j in range(data.shape[0]):
            df.loc[o_names[i], t_names[j]] = data[i, j]
    data = np.loadtxt(os.path.join(out_data_folder, "opt_transshipments_to_destinations.csv"),
                      delimiter=",")
    for i in range(data.shape[0]):
        for j in range(data.shape[0]):
            df.loc[t_names[i], d_names[j]] = data[i, j]
    data = np.loadtxt(os.path.join(out_data_folder, "opt_transshipments_to_transshipments.csv"),
                      delimiter=",")
    for i in range(data.shape[0]):
        for j in range(data.shape[0]):
            df.loc[t_names[i], t_names[j]] = data[i, j]
    # Write to excel
    writer = pd.ExcelWriter('opt_all.xlsx')
    df.to_excel(writer)
    writer.save()
    # Write to csv
    df.to_csv('opt_all.csv', sep=",")
    return
