#!/usr/bin/env python
# coding: utf-8

# In[ ]:


W@import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from optimizer import run_optimization, load_data

st.set_page_config(page_title="LineWise Optimizer", layout="wide")

st.title("LineWise — Production Recovery Optimizer")
st.write("Upload your equipment status CSV to find the optimal repair strategy.")

uploaded_file = st.file_uploader("Upload Equipment CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("### Current Equipment Status")
    st.dataframe(df)

    machines_dict = load_data(df)

    max_possible_cost = sum(
        m.repair_cost for m in machines_dict.values() if m.is_broken
    )

    st.sidebar.header("Maintenance Constraints")
    budget = st.sidebar.slider(
        "Available Budget ($)",
        min_value=0,
        max_value=max(500, int(max_possible_cost)),
        step=500
    )

    best_plan, total_cost, recovered_value = run_optimization(
        machines_dict, budget
    )

    st.write("---")
    st.subheader("Recommended Repair Strategy")

    if not best_plan:
        st.warning(
            "No repair combination restores production within the selected budget."
        )
    else:
        st.success(f"Total Production Value Restored: ${recovered_value:,}")
        st.info(f"Total Repair Cost: ${total_cost:,} (Out of ${budget:,} budget)")

        results_data = [
            {
                "Machine ID": m.machine_id,
                "Repair Cost": m.repair_cost,
                "Value Added": m.production_value
            }
            for m in best_plan
        ]

        results_df = pd.DataFrame(results_data)
        st.table(results_df)


fig, ax = plt.subplots(figsize=(8, 4))

        metrics = [
            "Maintenance Budget",
            "Total Repair Cost",
            "Production Restored"
        ]

        values = [budget, total_cost, recovered_value]
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

        ax.bar(metrics, values, color=colors)
        ax.set_ylabel("Amount ($)")
        ax.set_title("Financial Impact of Repair Strategy")

        st.pyplot(fig)
        plt.close(fig)







           csv_export = results_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Repair Plan as CSV",
            data=csv_export,
            file_name="linewise_optimal_repairs.csv",
            mime="text/csv"
        )


st.write("---")
    st.subheader("Budget Scenario Comparison")

    budgets = list(range(0, int(max_possible_cost) + 1, 500))

    # Include the exact maximum cost when not divisible by 500
    if budgets[-1] != int(max_possible_cost):
        budgets.append(int(max_possible_cost))

    recovery_values = []

    for budget_amount in budgets:
        plan, cost, recovered = run_optimization(
            machines_dict, budget_amount
        )
        recovery_values.append(recovered)

    fig2, ax2 = plt.subplots(figsize=(8, 4))

    ax2.plot(budgets, recovery_values, marker='o')
    ax2.set_xlabel("Maintenance Budget ($)")
    ax2.set_ylabel("Production Value Restored ($)")
    ax2.set_title("Budget vs. Production Recovery")
    ax2.grid(True)

    st.pyplot(fig2)
    plt.close(fig2)




# In[ ]:




