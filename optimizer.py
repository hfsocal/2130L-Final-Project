#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import itertools
import pandas as pd

class Machine:
    def __init__(self, machine_id, repair_cost, production_value, dependencies=None, is_broken=True):
        self.machine_id = machine_id
        self.repair_cost = repair_cost
        self.production_value = production_value
        # List of machine IDs that must be operational for this machine to generate value
        self.dependencies = dependencies if dependencies else []
        self.is_broken = is_broken

def run_optimization(machines_dict, budget):
    """
    Evaluates combinations of broken machines to maximize production recovery 
    without exceeding the maintenance budget and respecting AON-style dependencies.
    """
    broken_machines = [m for m in machines_dict.values() if m.is_broken]
    best_repair_plan = []
    max_recovered_value = 0
    total_repair_cost = 0

    # Evaluate all possible combinations of repairs
    for i in range(1, len(broken_machines) + 1):
        for combo in itertools.combinations(broken_machines, i):
            cost = sum(m.repair_cost for m in combo)

            if cost <= budget:
                combo_ids = {m.machine_id for m in combo}
                combo_prod_value = 0
                is_valid_combo = True

                # Check if dependencies are met for each machine in the proposed combo
                for m in combo:
                    deps_met = all(
                        (not machines_dict[dep].is_broken) or (dep in combo_ids)
                        for dep in m.dependencies
                    )

                    # If a required node is missing, this combination fails to restore the line
                    if not deps_met:
                        is_valid_combo = False
                        break

                    combo_prod_value += m.production_value

                if is_valid_combo and combo_prod_value > max_recovered_value:
                    max_recovered_value = combo_prod_value
                    best_repair_plan = combo
                    total_repair_cost = cost

    return best_repair_plan, total_repair_cost, max_recovered_value

def load_data(df):
    """Converts a Pandas DataFrame into a dictionary of Machine objects."""
    machines = {}
    for _, row in df.iterrows():
        # Handle empty dependencies in the CSV
        deps = []
        if pd.notna(row['Dependencies']):
            deps = [d.strip() for d in str(row['Dependencies']).split(',')]

        machines[row['Machine_ID']] = Machine(
            machine_id=row['Machine_ID'],
            repair_cost=row['Repair_Cost'],
            production_value=row['Production_Value'],
            dependencies=deps,
            is_broken=row['Is_Broken']
        )
    return machines



