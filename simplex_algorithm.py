import numpy as np

def solve(tableau,nb_vars):
    #as we want a minimizaion task we multiple c by -1
    tableau[0,1:nb_vars+1] = np.multiply(tableau[0,1:nb_vars+1],-1)
    while True:

        if all(tableau[0, 1:nb_vars+1] >= 0):
            print("Optimal Solution Found:")

            return np.zeros(nb_vars)#dummy response
        
        entering_var = np.argmin(tableau[0,1:(nb_vars+1)]) + 1 #selects column
        # Calculate the ratios
        ratios = tableau[1:, -1] / tableau[1:, entering_var]

        if np.all(ratios == np.inf):
            return "Problem is unbounded"
        
        # Choose the leaving variable (minimum positive ratio)
        leaving_var = np.argmin(ratios) + 1
        
        pivot_row = tableau[leaving_var, :]
        tableau[leaving_var, :] = pivot_row / pivot_row[entering_var]
        for i in range(nb_vars):
            if i != leaving_var:
                factor = tableau[i, entering_var]
                tableau[i, :] -= factor * tableau[leaving_var,:]
