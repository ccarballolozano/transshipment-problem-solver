from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
import os
from functions import getmethod, solve
import webbrowser
import pandas as pd


root_dir = os.path.dirname(os.path.abspath(__file__))
data_in_dir_rel = "data_in"
data_out_dir_rel = "data_out"
data_in_dir = os.path.join(root_dir, data_in_dir_rel)
data_out_dir = os.path.join(root_dir, data_out_dir_rel)

window = Tk()

window.title("Transshipment solver")

#window.geometry('350x200')

##############
stp_1_lbl = Label(window, text="Step 1: Select Data (skip if manually added data)")
stp_1_lbl.grid(column=0, row=0)
row_0 = 1
col_0 = 0

o_lbl = Label(window, text="Origins")
o_lbl.grid(column=0 + col_0, row=0 + row_0)
o_file = None


def o_btn_clicked():
    global o_file
    o_file_2 = filedialog.askopenfilename()
    if o_file_2 is not () or o_file_2 != "":
        o_file = o_file_2
        o_lbl.configure(text="Done !")


o_btn = Button(window, text="Select csv", command=o_btn_clicked)
o_btn.grid(column=1 + col_0, row=0 + row_0)

t_lbl = Label(window, text="Transshipments")
t_lbl.grid(column=0 + col_0, row=1 + row_0)
t_file = None


def t_btn_clicked():
    global t_file
    t_file_2 = filedialog.askopenfilename()
    if t_file_2 is not () or t_file_2 != "":
        t_file = t_file_2
        t_lbl.configure(text="Done !")


t_btn = Button(window, text="Select csv", command=t_btn_clicked)
t_btn.grid(column=1 + col_0, row=1 + row_0)

d_lbl = Label(window, text="Destinations")
d_lbl.grid(column=0 + col_0, row=2 + row_0)
d_file = None


def d_btn_clicked():
    global d_file
    d_file_2 = filedialog.askopenfilename()
    if d_file_2 is not () or d_file_2 != "":
        d_file = d_file_2
        d_lbl.configure(text="Done !")


d_btn = Button(window, text="Select csv", command=d_btn_clicked)
d_btn.grid(column=1 + col_0, row=2 + row_0)


def key_btn_clicked():
    global api_key
    api_key_2 = simpledialog.askstring(title="DistanceMatrix API key", prompt="Write key")
    if api_key_2 is not () or api_key_2 != "" or api_key_2 is None:
        api_key = api_key_2
        key_lbl.configure(text="Done !")


key_lbl = Label(window, text="DistanceMatrix API Key")
key_lbl.grid(column=0 + col_0, row=3 + row_0)
key_btn = Button(window, text="Put key", command=key_btn_clicked)
key_btn.grid(column=1 + col_0, row=3 + row_0)


def go_btn_clicked():
    global root_dir
    getmethod.from_maps_api(api_key, o_file, d_file, t_file, data_in_dir)
    key_btn.config(text="Done !")


go_btn = Button(window, text="Click when files selected", command=go_btn_clicked)
go_btn.grid(row=4 + row_0)

"""
Step 2
"""
row_0 = 6
col_0 = 0
stp_2_lbl = Label(window, text="Step 2: Add data manually or edit the imported")
stp_2_lbl.grid(row=row_0, column=col_0, columnspan=2)
stp_2_lbl_1 = Label(window, text="(i) Coming from Step 1, modify created files")
stp_2_lbl_1.grid(row=row_0 + 1, column=col_0, columnspan=2)
stp_2_lbl_2 = Label(window, text="(ii) If not, manually paste necessary data, see documentation")
stp_2_lbl_2.grid(row=row_0 + 2, column=col_0, columnspan=2)


def edit_btn_clicked():
    global data_in_dir
    webbrowser.open(data_in_dir)


edit_btn = Button(window, text="Edit Data", command=edit_btn_clicked)
edit_btn.grid(column=col_0, row=3 + row_0, columnspan=2)

"""
Step 3: Solve
"""
row_0 = 10
col_0 = 0


def run_btn_clicked():
    global data_in_dir
    global data_out_dir
    o_to_d = pd.read_csv(os.path.join(data_in_dir, "cost_origins_to_destinations.csv"), index_col=0).values
    o_to_t = pd.read_csv(os.path.join(data_in_dir, "cost_origins_to_transshipments.csv"), index_col=0).values
    t_to_d = pd.read_csv(os.path.join(data_in_dir, "cost_transshipments_to_destinations.csv"), index_col=0).values
    t_to_t = pd.read_csv(os.path.join(data_in_dir, "cost_transshipments_to_transshipments.csv"), index_col=0).values
    o_sup = pd.read_csv(os.path.join(data_in_dir, "supply_origins.csv"), index_col=0).values
    t_sup = pd.read_csv(os.path.join(data_in_dir, "supply_transshipments.csv"), index_col=0).values
    d_dem = pd.read_csv(os.path.join(data_in_dir, "demand_destinations.csv"), index_col=0).values
    t_dem = pd.read_csv(os.path.join(data_in_dir, "demand_transshipments.csv"), index_col=0).values
    o_to_d_cap = pd.read_csv(os.path.join(data_in_dir, "capacity_origins_to_destinations.csv"), index_col=0).values
    o_to_t_cap = pd.read_csv(os.path.join(data_in_dir, "capacity_origins_to_transshipments.csv"), index_col=0).values
    t_to_d_cap = pd.read_csv(os.path.join(data_in_dir, "capacity_transshipments_to_destinations.csv"), index_col=0).values
    t_to_t_cap = pd.read_csv(os.path.join(data_in_dir, "capacity_transshipments_to_transshipments.csv"), index_col=0).values
    opt_val, opt_o_to_d, opt_o_to_t, opt_t_to_d, opt_t_to_t, msg = solve.build_and_solve(
        o_to_d, o_to_t, t_to_t, t_to_d, o_sup, t_sup, d_dem, t_dem, o_to_d_cap, o_to_t_cap, t_to_d_cap, t_to_t_cap)
    o_id = pd.read_csv(os.path.join(data_in_dir, "id_origins.csv"), header=None)
    t_id = pd.read_csv(os.path.join(data_in_dir, "id_transshipments.csv"), header=None)
    d_id = pd.read_csv(os.path.join(data_in_dir, "id_destinations.csv"), header=None)
    solve.save_result(opt_val, opt_o_to_d, opt_o_to_t, opt_t_to_d, opt_t_to_t, o_id, d_id, t_id, data_out_dir)


run_btn = Button(window, text="Solve", command=run_btn_clicked)
run_btn.grid(column=col_0, row=3 + row_0, columnspan=2)

window.mainloop()
