from tkinter import *
from tkinter import filedialog
import os
from functions import getmethod, solve
import webbrowser
import pandas as pd
import shutil


def main():
    global data_in_dir, data_out_dir
    # root_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.getcwd()
    data_in_dir_rel = "data_in"
    data_out_dir_rel = "data_out"
    data_in_dir = os.path.join(root_dir, data_in_dir_rel)
    data_out_dir = os.path.join(root_dir, data_out_dir_rel)

    window = Tk()

    window.title("Transshipment solver")

    #window.geometry('350x200')

    ##############

    """
    HEADER.
    """
    row_0 = 0
    col_0 = 0
    header_lbl = Label(window, text="Solve your supply chain")
    header_lbl.grid(row=row_0, column=col_0, columnspan=2)
    header_email_label = Label(window, text="ccarballolozano@gmail.com")
    header_email_label.grid(row=row_0, column=2 + col_0)

    """
    INPUT FROM MAPS DISTANCEMATRIX API.
    """
    row_0 = 2
    col_0 = 0

    stp_1_lbl = Label(window, text="Build Data from Maps API (skip if manually)", font=("Arial Bold", 15))
    stp_1_lbl.grid(column=0, row=0 + row_0, columnspan=3)

    o_lbl = Label(window, text="Origins: ")
    o_lbl.grid(column=0 + col_0, row=1 + row_0)
    o_entry = Entry(window, width=30)
    o_entry.grid(column=1 + col_0, row=1 + row_0)

    def o_btn_clicked():
        ask = filedialog.askopenfilename()
        if ask is not () or ask != "":
            o_entry.delete(0, END)
            o_entry.insert(0, ask)

    o_btn = Button(window, text="Select csv", command=o_btn_clicked)
    o_btn.grid(column=2 + col_0, row=1 + row_0)

    t_lbl = Label(window, text="Transshipments: ")
    t_lbl.grid(column=0 + col_0, row=2 + row_0)
    t_entry = Entry(window, width=30)
    t_entry.grid(column=1 + col_0, row=2 + row_0)

    def t_btn_clicked():
        ask = filedialog.askopenfilename()
        if ask is not () or ask != "":
            t_entry.delete(0, END)
            t_entry.insert(0, ask)

    t_btn = Button(window, text="Select csv", command=t_btn_clicked)
    t_btn.grid(column=2 + col_0, row=2 + row_0)

    d_lbl = Label(window, text="Destinations")
    d_lbl.grid(column=0 + col_0, row=3 + row_0)
    d_entry = Entry(window, width=30)
    d_entry.grid(column=1 + col_0, row=3 + row_0)

    def d_btn_clicked():
        ask = filedialog.askopenfilename()
        if ask is not () or ask != "":
            d_entry.delete(0, END)
            d_entry.insert(0, ask)

    d_btn = Button(window, text="Select csv", command=d_btn_clicked)
    d_btn.grid(column=2 + col_0, row=3 + row_0)

    key_lbl = Label(window, text="DistanceMatrix API Key: ")
    key_lbl.grid(column=0 + col_0, row=4 + row_0)
    key_entry = Entry(window, width=30)
    key_entry.grid(column=1 + col_0, row=4 + row_0)

    def go_btn_clicked():
        global data_in_dir
        getmethod.from_maps_api(key_entry.get(), o_entry.get(), d_entry.get(), t_entry.get(), data_in_dir)

    go_btn = Button(window, text="Build Data", command=go_btn_clicked)
    go_btn.grid(row=5 + row_0, column=0 + col_0, columnspan=3)

    """
    EDIT INPUTS
    """
    row_0 = 8
    col_0 = 0
    stp_2_lbl = Label(window, text="Add data manually or edit the built one", font=("Arial Bold", 15))
    stp_2_lbl.grid(row=row_0, column=col_0, columnspan=3)
    stp_2_lbl_1 = Label(window, text="(i) Coming from Step 1, modify created files")
    stp_2_lbl_1.grid(row=row_0 + 1, column=col_0, columnspan=3)
    stp_2_lbl_2 = Label(window, text="(ii) If not, manually paste necessary data, see documentation")
    stp_2_lbl_2.grid(row=row_0 + 2, column=col_0, columnspan=3)

    def edit_btn_clicked():
        global data_in_dir
        webbrowser.open(data_in_dir)

    edit_btn = Button(window, text="Edit Data", command=edit_btn_clicked)
    edit_btn.grid(column=col_0, row=3 + row_0, columnspan=3)

    """
    Step 3: Solve
    """
    row_0 = 12
    col_0 = 0
    stp_3_lbl = Label(window, text="Get the optimal solution", font=("Arial Bold", 15))
    stp_3_lbl.grid(row=0 + row_0, column=0 + col_0, columnspan=3)

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
        solve.save_result(opt_val, opt_o_to_d, opt_o_to_t, opt_t_to_d, opt_t_to_t, data_out_dir, o_id, d_id, t_id)

    run_btn = Button(window, text="Optimize", command=run_btn_clicked)
    run_btn.grid(column=0 + col_0, row=1 + row_0, columnspan=3)

    """
    Step 4: Export result
    """
    row_0 = 14
    col_0 = 0
    stp_3_lbl = Label(window, text="Export Solution", font=("Arial Bold", 15))
    stp_3_lbl.grid(row=0 + row_0, column=0 + col_0, columnspan=3)

    export_dir_lbl = Label(window, text="Folder: ")
    export_dir_lbl.grid(row=1 + row_0, column=0 + col_0)
    export_dir_entry = Entry(window, width=15)
    export_dir_entry.grid(row=1 + row_0, column=1 + col_0)

    def export_dir_btn_clicked():
        ask = filedialog.askdirectory()
        export_dir_entry.delete(0, END)
        export_dir_entry.insert(0, ask)

    export_dir_btn = Button(window, text="Select folder", command=export_dir_btn_clicked)
    export_dir_btn.grid(row=1 + row_0, column=2 + col_0)

    export_name_lbl = Label(window, text="Name: ")
    export_name_lbl.grid(row=2 + row_0, column=0 + col_0)
    export_name_entry = Entry(window, width=15)
    export_name_entry.grid(row=2 + row_0, column=1 + col_0)

    def export_xlsx_btn_clicked():
        global data_out_dir
        export_dir = export_dir_entry.get()
        export_name = export_name_entry.get()
        from_file = os.path.join(data_out_dir, 'opt_all.xlsx')
        to_file = os.path.join(export_dir, export_name) + '.xlsx'
        shutil.copy(from_file, to_file)

    export_xlsx_btn = Button(window, text="to .xlsx", command=export_xlsx_btn_clicked)
    export_xlsx_btn.grid(row=3 + row_0, column=0 + col_0, columnspan=2)

    def export_csv_btn_clicked():
        global data_out_dir
        export_dir = export_dir_entry.get()
        export_name = export_name_entry.get()
        from_file = os.path.join(data_out_dir, 'opt_all.csv')
        to_file = os.path.join(export_dir, export_name) + '.csv'
        shutil.copy(from_file, to_file)

    export_csv_btn = Button(window, text="to .csv", command=export_csv_btn_clicked)
    export_csv_btn.grid(row=3 + row_0, column=1 + col_0, columnspan=2)

    window.mainloop()


if __name__ == "__main__":
    main()
