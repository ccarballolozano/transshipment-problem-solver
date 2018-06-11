import scipy as sp


def _parse_input_data(dir):
    """
    Returns costs, productions and demands as separate arrays
    """
    return o_to_d, o_to_t, t_to_t, o_prod, t_prod, d_dem, t_dem

# First are origins, then transshipments and finally destinations


def _build_coefficients():
    """
    Returns a 1-D array with coefficients
    """
    return c


def _build_constraint_1():
    return A_ub_1


def _build_constraint_2():
    return A_ub_2


def _build_constraint_3():
    return A_eq_1


def _build_constraint_4():
    return A_eq_2


def _build_A():
    return A_ub, A_eq


def _build_b():
    return b_ub, b_eq

def main(input_dir):
    o_to_d, o_to_t, t_to_t, o_prod, t_prod, d_dem, t_dem = _parse_input_data(input_dir)
    c = _build_coefficients(o_to_d, o_to_t, t_to_t)
    A_ub_1 = _build_constraint_1(o_prod, t_prod)
    A_ub_2 = _build_constraint_2(d_prod, t_prod)
    A_eq_1 = _build_constraint_3(d_dem, t_dem)
    A_eq_2 = _build_constraint_4(d_dem, t_dem)
    A_ub, A_eq = _build_A(A_ub_1, A_ub_2, A_eq_1, A_eq_2)
    b_ub, b_eq = _build_b()
