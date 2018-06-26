import numpy as np
from scipy.optimize import linprog
import os
import pandas as pd


def build_and_solve(o_to_d, o_to_t, t_to_t, t_to_d, o_prod, t_prod, d_dem, t_dem, o_to_d_cap, o_to_t_cap, t_to_d_cap, t_to_t_cap):
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

    # Organize functions that will be used
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

    def _build_bounds(o_to_d_cap, o_to_t_cap, t_to_d_cap, t_to_t_cap):
        upper_bounds = o_to_d_cap
        upper_bounds = np.concatenate((upper_bounds, o_to_t_cap), axis=1)
        aux = np.concatenate((t_to_d_cap, t_to_t_cap), axis=1)
        upper_bounds = np.concatenate((upper_bounds, aux), axis=0)
        upper_bounds = upper_bounds.reshape((-1))
        lower_bounds = np.full_like(upper_bounds, 0, dtype=np.int8)
        return list(zip(lower_bounds, upper_bounds))

    def _join_constraints(A_ub_1, A_ub_2, A_eq_1, A_eq_2, b_ub_1, b_ub_2, b_eq_1, b_eq_2):
        A_ub = np.concatenate((A_ub_1, A_ub_2), axis=0)
        b_ub = np.concatenate((b_ub_1, b_ub_2), axis=0)
        A_eq = np.concatenate((A_eq_1, A_eq_2), axis=0)
        b_eq = np.concatenate((b_eq_1, b_eq_2), axis=0)
        return A_ub, A_eq, b_ub, b_eq

    c = _build_coefficients(o_to_d, o_to_t, t_to_d, t_to_t)
    A_ub_1, b_ub_1 = _build_constraint_1(n_o, n_d, n_t, o_prod)
    A_ub_2, b_ub_2 = _build_constraint_2(n_o, n_d, n_t, t_prod)
    A_eq_1, b_eq_1 = _build_constraint_3(n_o, n_d, n_t, d_dem)
    A_eq_2, b_eq_2 = _build_constraint_4(n_o, n_d, n_t, t_dem)
    A_ub, A_eq, b_ub, b_eq = _join_constraints(
        A_ub_1, A_ub_2, A_eq_1, A_eq_2, b_ub_1, b_ub_2, b_eq_1, b_eq_2)
    bounds = _build_bounds(o_to_d_cap, o_to_t_cap, t_to_d_cap, t_to_t_cap)
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
    res = linprog(c, A_ub, b_ub, A_eq, b_eq, bounds, method="simplex")
    status_options = {0: "Optimization terminated successfully",
                      1: "Iteration limit reached",
                      2: "Problem appears to be infeasible",
                      3: "Problem appears to be unbounded"}
    if res.success:
        msg = "Optimization terminated successfully"
        print(msg)
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
        return opt_val, opt_o_to_d, opt_o_to_t, opt_t_to_d, opt_t_to_t, msg
    else:
        msg = status_options[res.status]
        print(msg)
        return -1, -1, -1, -1, -1, msg


def save_result(opt_val, opt_o_to_d, opt_o_to_t, opt_t_to_d, opt_t_to_t, to_folder, o_id=False, d_id=False, t_id=False):
    if o_id is not False:
        o_id = o_id.values[0]
    else:
        o_id = ["O" + str(i+1) for i in range(opt_o_to_d.shape[0])]
    if d_id is not False:
        d_id = d_id.values[0]
    else:
        d_id = ["D" + str(i+1) for i in range(opt_o_to_d.shape[1])]
    if t_id is not False:
        t_id = t_id.values[0]
    else:
        t_id = ["T" + str(i+1) for i in range(opt_o_to_t.shape[1])]

    if not os.path.exists(to_folder):
        os.makedirs(to_folder)
    else:
        for f in os.listdir(to_folder):
            if f.endswith(".csv") or f.endswith(".xlsx"):
                os.remove(os.path.join(to_folder, f))
    np.savetxt(os.path.join(to_folder, "opt_value.csv"),
               np.array(opt_val).reshape((-1)), fmt="%f", delimiter=",")
    np.savetxt(os.path.join(to_folder, "opt_origins_to_destinations.csv"),
               opt_o_to_d, fmt="%f", delimiter=",")
    np.savetxt(os.path.join(to_folder, "opt_origins_to_transshipments.csv"),
               opt_o_to_t, fmt="%f", delimiter=",")
    np.savetxt(os.path.join(to_folder, "opt_transshipments_to_destinations.csv"),
               opt_t_to_d, fmt="%f", delimiter=",")
    np.savetxt(os.path.join(to_folder, "opt_transshipments_to_transshipments.csv"),
               opt_t_to_t, fmt="%f", delimiter=",")
    rows = np.concatenate((o_id, t_id))
    cols = np.concatenate((d_id, t_id))
    df = pd.DataFrame(index=rows, columns=cols)
    data = np.loadtxt(os.path.join(to_folder, "opt_origins_to_destinations.csv"),
                      delimiter=",")
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            df.loc[o_id[i], d_id[j]] = data[i, j]
    data = np.loadtxt(os.path.join(to_folder, "opt_origins_to_transshipments.csv"),
                      delimiter=",")
    # print(data)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            df.loc[o_id[i], t_id[j]] = data[i, j]
    data = np.loadtxt(os.path.join(to_folder, "opt_transshipments_to_destinations.csv"),
                      delimiter=",")
    # print(data)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            df.loc[t_id[i], d_id[j]] = data[i, j]
    data = np.loadtxt(os.path.join(to_folder, "opt_transshipments_to_transshipments.csv"),
                      delimiter=",")
    # print(data)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            df.loc[t_id[i], t_id[j]] = data[i, j]
    # Write to excel

    writer = pd.ExcelWriter(os.path.join(to_folder, 'opt_all.xlsx'))
    df.to_excel(writer)
    writer.save()
    # Write to csv
    df.to_csv(os.path.join(to_folder, 'opt_all.csv'), sep=",")
    return
