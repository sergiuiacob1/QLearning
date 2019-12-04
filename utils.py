def build_empty_matrix(n_lins, n_cols):
    A = [None] * n_lins
    for i in range(0, n_lins):
        A[i] = [0] * n_cols
    return A
