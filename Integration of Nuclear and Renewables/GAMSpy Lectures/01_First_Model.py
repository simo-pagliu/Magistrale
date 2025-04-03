# Install GAMSPy: pip install gamspy
# GAMS: General Algebraic Modelling System
# Used to run optimization models
# Import the GAMSPy module
from __future__ import annotations

import pandas as pd

from gamspy import (
    Container,
    Equation,
    Model,
    Parameter,
    Sense,
    Set,
    Sum,
    Variable,
)

def load_data():
    capacity = pd.DataFrame(data=[["seattle", 350], ["san-diego", 600]], columns=["plant", "capacity"])
    demand = pd.DataFrame(data=[["new-york", 325], ["chicago", 300], ["topeka", 275]], columns=["market", "demand"])
    distance = pd.DataFrame(data=[
        ["seattle", "new-york", 2.5], 
        ["seattle", "chicago", 1.7], 
        ["seattle", "topeka", 1.8], 
        ["san-diego", "new-york", 2.5], 
        ["san-diego", "chicago", 1.8], 
        ["san-diego", "topeka", 1.4]], 
        columns=["plant", "market", "distance"])
    
    cost = 90 * distance.set_index(["plant", "market"])/1000

    return capacity, demand, distance, cost

container = Container()

plants = Set(container, name="plants", description="Canning plants")
markets = Set(container, name="markets", description="Markets")

supply = Parameter(container, name="supply", domain=plants, description="Capacity of plant i in cases")
demand = Parameter(container, name="demand", domain=markets, description="Demand at market j in cases")
ship_cost = Parameter(container, name="ship_cost", domain=[plants, markets], description="Shipping cost in dollars per case")

# Declare optimization Variable
optimized_shipment = Variable(container, type = "positive", name="optimized_shipment", domain=[plants, markets], description="Shipment quantities from plant to market in cases")

# Declare equations
supply_eq = Equation(container, name="supply_eq", domain=plants)
demand_eq = Equation(container, name="demand_eq", domain=markets)

# Define equations
supply_eq[plants] = Sum(markets, optimized_shipment[plants, markets]) <= supply[plants]
demand_eq[markets] = Sum(plants, optimized_shipment[plants, markets]) >= demand[markets]

# Define objective function
total_Cost = Sum([plants, markets], ship_cost[plants, markets] * optimized_shipment[plants, markets])

# Define Model
transport = Model(container, 
                  name="Transportation_Problem", 
                  equations=container.getEquations(),
                  sense=Sense.MIN, # Minimize the cost
                  problem="LP", # Linear Programming
                  objective=total_Cost)

# Load data
capacity_data, demand_data, distance_data, cost_data = load_data()
#
plants.setRecords(capacity_data["plant"].values)
markets.setRecords(demand_data["market"].values)
#
supply.setRecords(capacity_data)
demand.setRecords(demand_data[["market", "demand"]])
ship_cost.setRecords(cost_data["distance"])

# Solve the model
transport.solve(solver="CPLEX")

# Print the results
print("Status: ", transport.status)
print("\n")

print("Objective value: ", transport.objective_value)
print("\n")

print("Shipment quantities: ", optimized_shipment.records)
print("\n")

print("Pivot table: ", optimized_shipment.pivot())
print("\n")

# import sys
# transport.solve(output=sys.stdout, solver="CPLEX")