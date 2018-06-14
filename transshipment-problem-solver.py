from scipy.optimize import linprog
import numpy as np
import pandas as pd
import os
from lib import getmethod
import argparse


def _parse_input_data(in_data_folder):
    """
    Returns costs, productions and demands as separate numpy arrays.
    It also recomputes production and demand of transshipments by
    difference between them and adding the value L.
    """
    o_to_d = pd.read_csv(os.path.join(
        in_data_folder, "cost_origins_to_destinations.csv"), header=None)
    o_to_d = o_to_d.values
    o_to_t = pd.read_csv(os.path.join(
        in_data_folder, "cost_origins_to_transshipments.csv"), header=None)
    o_to_t = o_to_t.values
    t_to_t = pd.read_csv(os.path.join(
        in_data_folder, "cost_transshipments_to_transshipments.csv"), header=None)
    t_to_t = t_to_t.values
    t_to_d = pd.read_csv(os.path.join(
        in_data_folder, "cost_transshipments_to_destinations.csv"), header=None)
    t_to_d = t_to_d.values
    o_prod = pd.read_csv(os.path.join(
        in_data_folder, "production_origins.csv"), header=None)
    o_prod = o_prod.values.reshape((-1))
    t_prod = pd.read_csv(os.path.join(
        in_data_folder, "production_transshipments.csv"), header=None)
    t_prod = t_prod.values.reshape((-1))
    d_dem = pd.read_csv(os.path.join(
        in_data_folder, "demand_destinations.csv"), header=None)
    d_dem = d_dem.values.reshape((-1))
    t_dem = pd.read_csv(os.path.join(
        in_data_folder, "demand_transshipments.csv"), header=None)
    t_dem = t_dem.values.reshape((-1))
    n_o = o_to_d.shape[0]
    n_d = o_to_d.shape[1]
    n_t = o_to_t.shape[1]
    # productions and demands from transshipments can be made net
    for i in range(len(t_prod)):
        if t_prod[i] >= t_dem[i]:
            t_prod[i] = t_prod[i] - t_dem[i]
            t_dem[i] = 0
        else:
            t_prod[i] = 0
            t_dem[i] = t_dem[i] - t_prod[i]
    # now add L value which arises from transshipment to transportation
    L = np.sum(o_prod) + np.sum(t_prod)
    t_prod = t_prod + L
    t_dem = t_dem + L
    return o_to_d, o_to_t, t_to_t, t_to_d, o_prod, t_prod, d_dem, t_dem, n_o, n_d, n_t, L

# First are origins, then transshipments and finally destinations


def _build_coefficients(o_to_d, o_to_t, t_to_d, t_to_t):
    """
    Returns a 1-D array with coefficients
    O1D1,...,O1Dn,O1T1,...,O1Ts,O2D1,...O2Ts,...OmTs,T1D1,...T1Ts,...TsD1,...,TsDs
    """
    c = o_to_d
    c = np.concatenate((c, o_to_t), axis=1)
    aux = np.concatenate((t_to_d, t_to_t), axis=1)
    c = np.concatenate((c, aux), axis=0)
    c = c.reshape((-1))
    print(c)
    return c


def _build_constraint_1(n_o, n_d, n_t, o_prod):
    """
    Production at origins
    """
    n_vars = (n_o + n_t) * (n_d + n_t)
    b_ub_1 = o_prod
    A_ub_1 = np.zeros(shape=(n_o, n_vars))
    for i in range(n_o):
        # origin i to destinations
        A_ub_1[i, (i * (n_d + n_t)): (i * (n_d + n_t) + n_d)] = 1
        # origin i to transshipments
        A_ub_1[i, (i * (n_d + n_t) + n_d): (i * (n_d + n_t) + n_d + n_t)] = 1
    return A_ub_1, b_ub_1


def _build_constraint_2(n_o, n_d, n_t, t_prod):
    """
    Production at transshipments.
    """
    n_vars = (n_o + n_t) * (n_d + n_t)
    b_ub_2 = t_prod
    A_ub_2 = np.zeros(shape=(n_t, n_vars))
    for i in range(n_t):
        # transshipment i to destinations
        A_ub_2[i, ((n_o + i) * (n_d + n_t)):
               ((n_o + i) * (n_d + n_t) + n_d)] = 1
        # transshipment i to transshipments
        A_ub_2[i, ((n_o + i) * (n_d + n_t) + n_d):
               ((n_o + i) * (n_d + n_t) + n_d + n_t)] = 1
    return A_ub_2, b_ub_2


def _build_constraint_3(n_o, n_d, n_t, d_dem):
    n_vars = (n_o + n_t) * (n_d + n_t)
    b_eq_1 = d_dem
    A_eq_1 = np.zeros(shape=(n_d, n_vars))
    for i in range(n_d):
        # origins to destination i
        for j in range(n_o):
            A_eq_1[i, j * (n_d + n_t) + i] = 1  # origin j
        # transshipments to destination i
        for j in range(n_t):
            A_eq_1[i, (n_o + j) * (n_d + n_t) + i] = 1  # transshipment j
    return A_eq_1, b_eq_1


def _build_constraint_4(n_o, n_d, n_t, t_dem):
    n_vars = (n_o + n_t) * (n_d + n_t)
    b_eq_2 = t_dem
    A_eq_2 = np.zeros(shape=(n_t, n_vars))
    for i in range(n_t):
        # origins to transshipment i
        for j in range(n_o):
            A_eq_2[i, j * (n_d + n_t) + n_d + i] = 1  # origin j
        # transshipments to transshipmment i
        for j in range(n_t):
            A_eq_2[i, (n_o + j) * (n_d + n_t) + n_d + i] = 1  # transshipment j
    return A_eq_2, b_eq_2


def _join_constraints(A_ub_1, A_ub_2, A_eq_1, A_eq_2,
                      b_ub_1, b_ub_2, b_eq_1, b_eq_2):
    A_ub = np.concatenate((A_ub_1, A_ub_2), axis=0)
    b_ub = np.concatenate((b_ub_1, b_ub_2), axis=0)
    A_eq = np.concatenate((A_eq_1, A_eq_2), axis=0)
    b_eq = np.concatenate((b_eq_1, b_eq_2), axis=0)
    return A_ub, A_eq, b_ub, b_eq


def build_and_solve(in_data_folder):
    o_to_d, o_to_t, t_to_t, t_to_d, o_prod, t_prod, d_dem, t_dem, n_o, n_d, n_t, L = _parse_input_data(in_data_folder)
    c = _build_coefficients(o_to_d, o_to_t, t_to_d, t_to_t)
    A_ub_1, b_ub_1 = _build_constraint_1(n_o, n_d, n_t, o_prod)
    A_ub_2, b_ub_2 = _build_constraint_2(n_o, n_d, n_t, t_prod)
    A_eq_1, b_eq_1 = _build_constraint_3(n_o, n_d, n_t, d_dem)
    A_eq_2, b_eq_2 = _build_constraint_4(n_o, n_d, n_t, t_dem)
    A_ub, A_eq, b_ub, b_eq = _join_constraints(
        A_ub_1, A_ub_2, A_eq_1, A_eq_2, b_ub_1, b_ub_2, b_eq_1, b_eq_2)
    """ When errors arise, check this 
    np.savetxt("c.csv", c, fmt="%i", delimiter=",")
    np.savetxt("A_ub_1.csv", A_ub_1, fmt="%i", delimiter=",")
    np.savetxt("A_ub_2.csv", A_ub_2, fmt="%i", delimiter=",")
    np.savetxt("A_eq_1.csv", A_eq_1, fmt="%i", delimiter=",")
    np.savetxt("A_eq_2.csv", A_eq_2, fmt="%i", delimiter=",")
    np.savetxt("b_ub_1.csv", b_ub_1, fmt="%i", delimiter=",")
    np.savetxt("b_ub_2.csv", b_ub_2, fmt="%i", delimiter=",")
    np.savetxt("b_eq_1.csv", b_eq_1, fmt="%i", delimiter=",")
    np.savetxt("b_eq_2.csv", b_eq_2, fmt="%i", delimiter=",")
    """
    res = linprog(c, A_ub, b_ub, A_eq, b_eq)
    status_options = {0: "Optimization terminated successfully",
                      1: "Iteration limit reached",
                      2: "Problem appears to be infeasible",
                      3: "Problem appears to be unbounded"}
    if res.success:
        print("Optimization terminated successfully")
        opt_val = res.fun
        print("Optimal value is %f" % (opt_val))
        res_x = np.array(res.x)
        res_x = res_x.reshape((n_o + n_t, n_d + n_t))
        opt_o_to_d = res_x[: n_o, : n_d]
        opt_o_to_t = res_x[: n_o, n_d:]
        opt_t_to_d = res_x[n_o:, : n_d]
        opt_t_to_t = res_x[n_o:, n_d:]
        # Substract L to the variables affected by the variable change
        for i in range(opt_t_to_t.shape[0]):
            opt_t_to_t[i, i] = L - opt_t_to_t[i, i]
        return opt_val, opt_o_to_d, opt_o_to_t, opt_t_to_d, opt_t_to_t
    else:
        print(status_options[res.status])
        return -1, -1, -1, -1, -1


def _output_results(out_data_folder, opt_val, opt_o_to_d, opt_o_to_t, opt_t_to_d, opt_t_to_t):
    np.savetxt(os.path.join(out_data_folder, "opt_value.csv"),
               np.array(opt_val).reshape((-1)), fmt="%10.4f", delimiter=",")
    np.savetxt(os.path.join(out_data_folder, "opt_origins_to_destinations.csv"),
               opt_o_to_d, fmt="%10.4f", delimiter=",")
    np.savetxt(os.path.join(out_data_folder, "opt_origins_to_transshipments.csv"),
               opt_o_to_t, fmt="%10.4f", delimiter=",")
    np.savetxt(os.path.join(out_data_folder, "opt_transshipments_to_destinations.csv"),
               opt_t_to_d, fmt="%10.4f", delimiter=",")
    np.savetxt(os.path.join(out_data_folder, "opt_transshipments_to_transshipments.csv"),
               opt_t_to_t, fmt="%10.4f", delimiter=",")


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--getmethod",
                        help="get data method", type=str, default="default")
    parser.add_argument("-c", "--costperkm",
                        help="cost per km distance", type=float, default=1)
    parser.add_argument("-k", "--keyfile",
                        help="maps distancematrix API key file", type=str, default="distancematrix_api_key.txt")
    return parser.parse_args()


def main(args):
    if args.getmethod == "default":
        pass
    elif args.getmethod == "maps":
        getmethod.from_maps_api(
            args.costperkm, args.keyfile, "data_in", "data_in")
    else:
        print("Not a valid get data method")
    opt_val, opt_o_to_d, opt_o_to_t, opt_t_to_d, opt_t_to_t = build_and_solve("data_in")
    if opt_val == -1:
        return
    else:
        pass
    _output_results("data_out", opt_val, opt_o_to_d,
                    opt_o_to_t, opt_t_to_d, opt_t_to_t)
    return


if __name__ == "__main__":
    args = parse_arguments()
    main(args)
