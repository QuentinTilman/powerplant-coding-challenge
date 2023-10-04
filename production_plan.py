import numpy as np
import simplex_algorithm


# For this optimization problem we take the approach to use a simplex algorithm

def create_initial_tableau(data):
    load = data["load"]
    fuels = data["fuels"]
    powerplants = data["powerplants"]
    nb_pp = len(powerplants)

    # We start by translating for each powerplant its cost per unit of generated electricity.
    # Using this method we create our cost vector (for sake of simplicity we reduce the cost to Integers)
    c = []
    for pp in powerplants:
        cost = cost_per_unit(fuels,pp)
        c.append(cost)
    c = np.array(c)

    # now we translate our constraints
    # Our first constraint is the load => x_1 + x_2 + x_3 + .. +x_n = load
    # Second is the Pmax constraint, for each powerplant => x_i <= Pmax_i 
    # at last possible Pmin constraint for gas based powerplants => x_ig >= Pmin (Only if used)
    # All constraint are in vector b with each powerplant having max 2 constraints

    b = np.zeros(1)#initial 0 for cost function
    b = np.vstack((b,[load]))
    for i in range(nb_pp):
        constraint = []
        if(powerplants[i]["type"] == "gasfired"):
           constraint = np.array(([powerplants[i]["pmax"]],[-1*powerplants[i]["pmin"]]))
        else:
           constraint = np.array([powerplants[i]["pmax"]])
        b = np.vstack((b,constraint))
    m,_ = b.shape


    # We now generate A
    A = np.zeros(m-2) # zeros for cost function
    #we add load constraint
    A = np.vstack((A,np.ones(m-2)))
    # Here we create A with certain variables subject to two constraints
    for i in range(0,m-2):
        row = np.zeros(m-2)
        if(b[i+2]< 0):
            row[i-1] = 1
        else:
            row[i] = 1
        A = np.vstack((A,row))
    
    
    
   
    # Here we need to create a special matrix as certain slack variables are subject to two constraints, if <= then 1 if >= then -1
    # we make use of the minus sign on the constraint values to update the slack variable value
    m,_ = A.shape
    slack_vars = np.eye(m)
    slack_vars[1,:] = np.zeros(m) # second row is constraint on load, may not have slack as we want it to be equal
    for i in range(2,m):
        if(b[i]<0):
            slack_vars[i,slack_vars[i,:] == 1] *= -1
            b[i] *= -1
    

    #we create lower_rows from initial tableau
    first_column = np.zeros((m,1)) # for cost function
    tableau = np.hstack((first_column,A,slack_vars))
    
    #first add slach for C then zeros for other slack variables
    c = np.hstack(([1],c,np.zeros(m)))
    
    tableau[0,:len(c)] = c

    #add b to tableau
    tableau = np.hstack((tableau,b))
    print(tableau.shape)
    return tableau,nb_pp
    
    

def cost_per_unit(prices,powerplant):
    fuel_type = powerplant["type"]
    efficiency = powerplant["efficiency"]
    cost = 0.0
    if fuel_type == "gasfired":
        cost = prices["gas(euro/MWh)"]
    if fuel_type == "turbojet":
        cost = prices["kerosine(euro/MWh)"]
    return int(cost*1/efficiency)


def culculate_production(data):
    tableau, nb_vars = create_initial_tableau(data)
    solution = simplex_algorithm.solve(tableau,nb_vars)
    powerplants = data["powerplants"]
    response = [{"name": powerplants[i]["name"],"p":solution[i]} for i in range(nb_vars)]
    return response
