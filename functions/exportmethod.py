import numpy as np
import os
import pandas as pd


def to_complete_file(out_data_folder, o_id, d_id, t_id):
    rows = o_id + t_id
    cols = d_id + t_id
    df = pd.DataFrame(index=rows, columns=cols)
    data = np.loadtxt(os.path.join(out_data_folder, "opt_origins_to_destinations.csv"),
                      delimiter=",")
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            df.loc[o_id[i], d_id[j]] = data[i, j]
    data = np.loadtxt(os.path.join(out_data_folder, "opt_origins_to_transshipments.csv"),
                      delimiter=",")
    # print(data)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            df.loc[o_id[i], t_id[j]] = data[i, j]
    data = np.loadtxt(os.path.join(out_data_folder, "opt_transshipments_to_destinations.csv"),
                      delimiter=",")
    # print(data)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            df.loc[t_id[i], d_id[j]] = data[i, j]
    data = np.loadtxt(os.path.join(out_data_folder, "opt_transshipments_to_transshipments.csv"),
                      delimiter=",")
    # print(data)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            df.loc[t_id[i], t_id[j]] = data[i, j]
    # Write to excel
    writer = pd.ExcelWriter(os.path.join("data_out", 'opt_all.xlsx'))
    df.to_excel(writer)
    writer.save()
    # Write to csv
    df.to_csv(os.path.join("data_out", 'opt_all.csv'), sep=",")
    return
